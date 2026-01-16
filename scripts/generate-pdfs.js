const { chromium } = require('playwright');
const express = require('express');
const path = require('path');
const fs = require('fs').promises;

async function generatePDFs() {
  const app = express();
  const port = 3001;

  // Serve the built web app
  app.use(express.static(path.join(__dirname, '../web/dist')));

  // Start server
  const server = app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
  });

  try {
    console.log('Installing Playwright browsers...');
    const { execSync } = require('child_process');
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

      await page.goto(url, { waitUntil: 'networkidle' });

      // Wait for content to load
      await page.waitForTimeout(2000);

      // Generate PDF
      await page.pdf({
        path: path.join(__dirname, `../docs/pdf/${dimension.filename}`),
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
      console.log(`✓ Generated ${dimension.filename}`);
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
