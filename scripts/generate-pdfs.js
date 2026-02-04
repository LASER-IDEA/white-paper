const { chromium } = require('playwright');
const express = require('express');
const path = require('path');
const fs = require('fs').promises;
const { spawnSync } = require('child_process');

async function generatePDFs() {
  const app = express();
  const port = 3001;

  // Temporarily rebuild the web app with base path '/' for local PDF generation
  console.log('Building web app for PDF generation...');
  const originalDir = process.cwd();
  process.chdir(path.join(__dirname, '../web'));

  try {
    // Temporarily modify vite.config.ts for local PDF generation
    const viteConfigPath = 'vite.config.ts';
    const viteConfigContent = require('fs').readFileSync(viteConfigPath, 'utf8');
    const originalConfigContent = viteConfigContent;

    console.log('Original vite config base path check:', viteConfigContent.includes("base: '/white-paper/'"));

    // Replace base path temporarily
    const tempConfigContent = viteConfigContent.replace("base: '/white-paper/',", "base: '/',");
    require('fs').writeFileSync(viteConfigPath, tempConfigContent);

    console.log('Modified vite config, building with base path: /');

    // Clean and build with temporary config
    try {
      // Clean dist directory
      const rmResult = spawnSync('rm', ['-rf', 'dist'], { stdio: 'inherit' });
      if (rmResult.error) {
        throw rmResult.error;
      }
      
      // Build the project
      const buildResult = spawnSync('npm', ['run', 'build'], { stdio: 'inherit' });
      if (buildResult.error || buildResult.status !== 0) {
        throw new Error(`Build failed with status ${buildResult.status}`);
      }
    } catch (buildError) {
      console.error('Build failed:', buildError);
      // Restore config even if build fails
      require('fs').writeFileSync(viteConfigPath, originalConfigContent);
      throw buildError;
    }

    // Restore original config
    require('fs').writeFileSync(viteConfigPath, originalConfigContent);
    console.log('Restored original vite config');

    console.log('Web app built successfully for PDF generation');
  } catch (error) {
    console.error('Failed to build web app:', error);
    process.exit(1);
  }

  process.chdir(originalDir);

  // Serve the rebuilt web app
  app.use(express.static(path.join(__dirname, '../web/dist')));

  // Start server
  const server = app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
  });

  try {
    console.log('Installing Playwright browsers...');
    const installResult = spawnSync('npx', ['playwright', 'install', 'chromium'], { stdio: 'inherit' });
    if (installResult.error) {
      throw installResult.error;
    }

    // Launch browser
    const browser = await chromium.launch({
      headless: true,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-accelerated-2d-canvas',
        '--no-first-run',
        '--disable-gpu'
      ]
    });

    const dimensions = [
      // Removed 'All' dimension to avoid redundancy - the 5 dimensional PDFs will be merged
      // { name: 'All', param: '', filename: 'Low-Altitude Economy White Paper.pdf' },
      { name: '规模与增长', param: '规模与增长', filename: 'scale_growth_report.pdf' },
      { name: '结构与主体', param: '结构与主体', filename: 'structure_entity_report.pdf' },
      { name: '时空特征', param: '时空特征', filename: 'time_space_report.pdf' },
      { name: '效率与质量', param: '效率与质量', filename: 'efficiency_quality_report.pdf' },
      { name: '创新与融合', param: '创新与融合', filename: 'innovation_integration_report.pdf' }
    ];

    // Ensure output directory exists
    await fs.mkdir(path.join(__dirname, '../docs/pdf'), { recursive: true });

    for (const dimension of dimensions) {
      console.log(`Generating PDF for ${dimension.name}...`);

      const page = await browser.newPage();

      // Set viewport for A4
      await page.setViewportSize({
        width: Math.round(210 * 3.78), // A4 width in pixels at 96 DPI
        height: Math.round(297 * 3.78), // A4 height in pixels at 96 DPI
      });

      // Navigate to the page
      const url = dimension.param
        ? `http://localhost:${port}?dimension=${encodeURIComponent(dimension.param)}`
        : `http://localhost:${port}`;

      console.log(`Navigating to: ${url}`);
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });

      // Debug: Check initial page load
      console.log('Page loaded, checking basic content...');
      const initialCheck = await page.evaluate(() => ({
        title: document.title,
        hasBody: !!document.body,
        bodyChildren: document.body ? document.body.children.length : 0,
        hasScript: !!document.querySelector('script[src*="index"]'),
        readyState: document.readyState
      }));
      console.log('Initial page check:', initialCheck);

      // Wait for basic page load
      await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {
        console.log('Network idle timeout, continuing...');
      });

      // Wait for React app to load (with simpler conditions first)
      console.log('Waiting for React app to load...');
      try {
        await page.waitForFunction(() => {
          // Simpler check: just wait for the main content div to exist
          return !!document.querySelector('#main-content');
        }, { timeout: 15000 });

        console.log('✓ Main content found');

        // Then wait for some content to be rendered
        await page.waitForFunction(() => {
          const mainContent = document.querySelector('#main-content');
          return mainContent && mainContent.children.length > 0;
        }, { timeout: 10000 });

        console.log('✓ Content rendered');
      } catch (error) {
        console.log('Warning: React app loading timeout, proceeding with PDF generation anyway');
        console.log('Error details:', error.message);
      }

      // Inject Chinese font CSS
      await page.addStyleTag({
        content: `
          @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&display=swap');

          * {
            font-family: 'Noto Sans SC', 'WenQuanYi Zen Hei', 'WenQuanYi Micro Hei', 'Microsoft YaHei', 'SimHei', sans-serif !important;
          }

          body {
            font-family: 'Noto Sans SC', 'WenQuanYi Zen Hei', 'WenQuanYi Micro Hei', 'Microsoft YaHei', 'SimHei', sans-serif !important;
          }
        `
      });

      // Wait for fonts to load and charts to render
      console.log('Waiting for content and fonts to load...');
      await page.waitForTimeout(5000);

      // Additional wait for any dynamic content
      try {
        await page.waitForFunction(() => {
          // Check if charts or data visualization elements are loaded
          const charts = document.querySelectorAll('.echarts-for-react, canvas, svg');
          return charts.length > 0 || document.querySelector('#main-content')?.children.length > 0;
        }, { timeout: 5000 });
      } catch (error) {
        console.log('Dynamic content check timed out, proceeding with PDF generation');
      }

      // Debug: Take screenshot for troubleshooting
      try {
        await page.screenshot({ path: `debug-${dimension.name}.png`, fullPage: true });
        console.log(`✓ Screenshot saved: debug-${dimension.name}.png`);
      } catch (error) {
        console.log(`⚠️ Failed to save screenshot: ${error.message}`);
      }

      // Debug: Check page content before PDF generation
      const contentCheck = await page.evaluate(() => {
        const mainContent = document.querySelector('#main-content');
        const body = document.body;
        const root = document.querySelector('#root');
        return {
          title: document.title,
          url: window.location.href,
          bodyVisible: window.getComputedStyle(body || {}).visibility,
          bodyDisplay: window.getComputedStyle(body || {}).display,
          rootExists: !!root,
          rootChildren: root ? root.children.length : 0,
          mainContentExists: !!mainContent,
          mainContentChildren: mainContent ? mainContent.children.length : 0,
          bodyText: body?.textContent?.substring(0, 200) || '',
          hasCharts: !!document.querySelector('.echarts-for-react, canvas, svg'),
          hasError: !!document.querySelector('.error, .loading-error'),
          consoleErrors: window.consoleErrors || []
        };
      });

      console.log(`Page content check for ${dimension.name}:`, JSON.stringify(contentCheck, null, 2));

      // Fallback: if no content detected, wait a bit more and try again
      if (!contentCheck.mainContentExists || contentCheck.mainContentChildren === 0) {
        console.log('No content detected, waiting additional time...');
        await page.waitForTimeout(5000);

        const retryCheck = await page.evaluate(() => ({
          mainContentExists: !!document.querySelector('#main-content'),
          mainContentChildren: document.querySelector('#main-content')?.children.length || 0,
          bodyText: document.body?.textContent?.substring(0, 100) || ''
        }));

        console.log('Retry check:', retryCheck);

        if (!retryCheck.mainContentExists) {
          console.log('⚠️ Still no main content detected, but proceeding with PDF generation anyway');
        }
      }

      // Generate PDF (with fallback)
      const pdfPath = path.join(__dirname, `../docs/pdf/${dimension.filename}`);
      try {
        await page.pdf({
          path: pdfPath,
          format: 'A4',
          printBackground: true,
          margin: {
            top: '20mm',
            right: '20mm',
            bottom: '20mm',
            left: '20mm'
          },
          displayHeaderFooter: false,
          preferCSSPageSize: false
        });
        console.log(`✓ PDF generated successfully: ${dimension.filename}`);
      } catch (pdfError) {
        console.error(`✗ PDF generation failed for ${dimension.filename}:`, pdfError.message);
        throw pdfError;
      }

      await page.close();

      // Verify PDF was created and has content
      const fs = require('fs').promises;
      try {
        const stats = await fs.stat(pdfPath);
        console.log(`✓ Generated ${dimension.filename} (${stats.size} bytes)`);
        if (stats.size < 10000) {
          console.warn(`⚠️ Warning: PDF file is very small (${stats.size} bytes), might be blank`);
        }
      } catch (error) {
        console.error(`✗ Failed to verify ${dimension.filename}:`, error);
      }
    }

    await browser.close();
    console.log('All PDFs generated successfully!');

  } catch (error) {
    console.error('Error generating PDFs:', error);
    process.exit(1);
  } finally {
    server.close();
  }
}

generatePDFs();
