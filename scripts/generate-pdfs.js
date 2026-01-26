const { chromium } = require('playwright');
const express = require('express');
const path = require('path');
const fs = require('fs').promises;

async function generatePDFs() {
  const app = express();
  const port = 3001;

  // Temporarily rebuild the web app with base path '/' for local PDF generation
  console.log('Building web app for PDF generation...');
  const { execSync } = require('child_process');
  const originalDir = process.cwd();
  process.chdir(path.join(__dirname, '../web'));

  try {
    // Temporarily modify vite.config.ts for local PDF generation
    const viteConfigPath = 'vite.config.ts';
    const viteConfigContent = require('fs').readFileSync(viteConfigPath, 'utf8');

    // Replace base path temporarily
    const tempConfigContent = viteConfigContent.replace("base: '/white-paper/',", "base: '/',");
    require('fs').writeFileSync(viteConfigPath, tempConfigContent);

    // Build with temporary config
    execSync('npm run build', { stdio: 'inherit' });

    // Restore original config
    require('fs').writeFileSync(viteConfigPath, viteConfigContent);

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
    execSync('npx playwright install chromium', { stdio: 'inherit' });

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
      { name: 'All', param: '', filename: 'Low-Altitude Economy White Paper.pdf' },
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
      await page.goto(url, { waitUntil: 'networkidle' });

      // Wait for React app to fully load and render
      console.log('Waiting for React app to load...');
      await page.waitForFunction(() => {
        // Check if React has mounted and basic elements are present
        return document.querySelector('#main-content') &&
               document.querySelector('[role="main"]') &&
               window.getComputedStyle(document.body).visibility !== 'hidden';
      }, { timeout: 10000 });

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

      // Debug: Check page content before PDF generation
      const contentCheck = await page.evaluate(() => {
        const mainContent = document.querySelector('#main-content');
        const body = document.body;
        return {
          title: document.title,
          bodyVisible: window.getComputedStyle(body).visibility,
          mainContentExists: !!mainContent,
          mainContentChildren: mainContent ? mainContent.children.length : 0,
          bodyText: body.textContent?.substring(0, 200) || '',
          hasCharts: !!document.querySelector('.echarts-for-react, canvas, svg')
        };
      });

      console.log(`Page content check for ${dimension.name}:`, contentCheck);

      // Generate PDF
      const pdfPath = path.join(__dirname, `../docs/pdf/${dimension.filename}`);
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
