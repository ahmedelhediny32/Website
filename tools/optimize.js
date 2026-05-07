const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const targetDir = 'd:\\website\\assets\\img';

async function processDirectory(dir) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);
        if (stat.isDirectory()) {
            await processDirectory(filePath);
        } else if (filePath.match(/\.(png|jpg|jpeg)$/i)) {
            // Only process large files (> 300KB) to save time and avoid re-compressing small icons
            if (stat.size > 300 * 1024) {
                console.log(`Optimizing: ${filePath} (${(stat.size / 1024 / 1024).toFixed(2)} MB)`);
                const tempPath = filePath + '.temp';
                try {
                    const ext = path.extname(filePath).toLowerCase();
                    let transformer = sharp(filePath);
                    
                    // Resize if too large
                    const metadata = await transformer.metadata();
                    if (metadata.width > 1200) {
                        transformer = transformer.resize(1200, null, { withoutEnlargement: true });
                    }

                    // Compress keeping original extension
                    if (ext === '.png') {
                        transformer = transformer.png({ quality: 75, compressionLevel: 8 });
                    } else if (ext === '.jpg' || ext === '.jpeg') {
                        transformer = transformer.jpeg({ quality: 75 });
                    }

                    await transformer.toFile(tempPath);
                    fs.unlinkSync(filePath);
                    fs.renameSync(tempPath, filePath);
                } catch (e) {
                    console.error(`Failed to process ${filePath}:`, e);
                    if (fs.existsSync(tempPath)) fs.unlinkSync(tempPath);
                }
            }
        }
    }
}

processDirectory(targetDir).then(() => {
    console.log("Optimization complete!");
});
