// static/admin/js/drag-drop.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing drag-drop...');
    initDragDrop();
});

function initDragDrop() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    console.log('Found file inputs:', fileInputs.length);
    
    fileInputs.forEach((input, index) => {
        console.log(`Processing input ${index}:`, input);
        
        if (input.dataset.dragEnabled) return;
        input.dataset.dragEnabled = 'true';
        
        // Находим контейнер поля
        const container = input.closest('.form-row') || input.closest('.field-image') || input.parentNode;
        console.log('Container:', container);
        
        if (!container) {
            console.log('No container found for input');
            return;
        }
        
        // Создаем зону
        const dropArea = document.createElement('div');
        dropArea.className = 'drag-drop-area';
        dropArea.innerHTML = `
            <div class="drag-drop-text">Перетащите изображение в эту область</div>
            <div class="upload-hint">или используйте кнопку ниже</div>
            <div class="file-name"></div>
        `;
        
        // Вставляем зону ПЕРЕД всем блоком с полем ввода
        container.parentNode.insertBefore(dropArea, container);
        console.log('Drop area inserted before container');
        
        // События
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(event => {
            dropArea.addEventListener(event, preventDefaults);
        });
        
        ['dragenter', 'dragover'].forEach(event => {
            dropArea.addEventListener(event, () => {
                console.log('Drag over');
                dropArea.classList.add('dragover');
            });
        });
        
        ['dragleave', 'drop'].forEach(event => {
            dropArea.addEventListener(event, () => {
                console.log('Drag leave/drop');
                dropArea.classList.remove('dragover');
            });
        });
        
        dropArea.addEventListener('drop', (e) => {
            console.log('File dropped');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                input.files = files;
                updateFileName(input, dropArea);
                
                // Создаем событие change
                const event = new Event('change', { bubbles: true });
                input.dispatchEvent(event);
            }
        });
        
        input.addEventListener('change', () => {
            console.log('File selected via button');
            updateFileName(input, dropArea);
        });
    });
}

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function updateFileName(input, dropArea) {
    const fileNameDiv = dropArea.querySelector('.file-name');
    
    if (input.files.length > 0) {
        const file = input.files[0];
        fileNameDiv.textContent = `Выбран файл: ${file.name}`;
        
        if (file.type.startsWith('image/')) {
            showPreview(file, dropArea);
        }
    } else {
        fileNameDiv.textContent = '';
        removePreview(dropArea);
    }
}

function showPreview(file, dropArea) {
    removePreview(dropArea);
    
    const reader = new FileReader();
    reader.onload = (e) => {
        const img = document.createElement('img');
        img.src = e.target.result;
        img.className = 'image-preview';
        dropArea.appendChild(img);
    };
    reader.readAsDataURL(file);
}

function removePreview(dropArea) {
    const oldPreview = dropArea.querySelector('.image-preview');
    if (oldPreview) oldPreview.remove();
}