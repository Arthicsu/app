document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-input');
    const fileList = document.getElementById('file-list');

    fileInput.addEventListener('change', () => {
        fileList.innerHTML = '';
        Array.from(fileInput.files).forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.innerHTML = `
                <span>${file.name}</span>
                <span>(${(file.size / 1024).toFixed(2)} KB)</span>
            `;
            fileList.appendChild(fileItem);
        });
    });
});