const fs = require('fs');
const path = require('path');

// Function to recursively find all .svelte files
function findSvelteFiles(dir, fileList = []) {
    const files = fs.readdirSync(dir);
    
    files.forEach(file => {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);
        
        if (stat.isDirectory() && !filePath.includes('node_modules') && !filePath.includes('.svelte-kit')) {
            findSvelteFiles(filePath, fileList);
        } else if (file.endsWith('.svelte')) {
            fileList.push(filePath);
        }
    });
    
    return fileList;
}

// Function to replace color classes in a file
function replaceColorsInFile(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');
    let originalContent = content;
    
    // Replace bg-gray-850 with bg-gray-800
    content = content.replace(/bg-gray-850/g, 'bg-gray-800');
    
    // Replace dark:bg-gray-850 with dark:bg-gray-800
    content = content.replace(/dark:bg-gray-850/g, 'dark:bg-gray-800');
    
    // Replace hover:bg-gray-850 with hover:bg-gray-800
    content = content.replace(/hover:bg-gray-850/g, 'hover:bg-gray-800');
    
    // Replace dark:hover:bg-gray-850 with dark:hover:bg-gray-800
    content = content.replace(/dark:hover:bg-gray-850/g, 'dark:hover:bg-gray-800');
    
    // Replace border-gray-850 with border-gray-800
    content = content.replace(/border-gray-850/g, 'border-gray-800');
    
    // Replace dark:border-gray-850 with dark:border-gray-800
    content = content.replace(/dark:border-gray-850/g, 'dark:border-gray-800');
    
    // Replace data-selected:bg-gray-850 with data-selected:bg-gray-800
    content = content.replace(/data-selected:bg-gray-850/g, 'data-selected:bg-gray-800');
    
    // Replace dark:data-selected:bg-gray-850 with dark:data-selected:bg-gray-800
    content = content.replace(/dark:data-selected:bg-gray-850/g, 'dark:data-selected:bg-gray-800');
    
    if (content !== originalContent) {
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`Updated: ${filePath}`);
        return true;
    }
    
    return false;
}

// Main execution
const componentsDir = path.join(__dirname, 'src/lib/components');
const svelteFiles = findSvelteFiles(componentsDir);

console.log(`Found ${svelteFiles.length} Svelte files`);

let updatedCount = 0;
svelteFiles.forEach(file => {
    if (replaceColorsInFile(file)) {
        updatedCount++;
    }
});

console.log(`\nUpdated ${updatedCount} files`);
console.log('Color scheme migration completed!');