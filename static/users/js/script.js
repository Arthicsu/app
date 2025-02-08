document.addEventListener('DOMContentLoaded', () => {
    const studentForm = document.getElementById('studentForm');
    const errorElement = document.getElementById('error-message');
    const requiredFields = studentForm.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('error-field');
        }
    });

    if (!isValid) {
        errorElement.textContent = 'Заполните все обязательные поля';
        errorElement.style.display = 'block';
        return;
    }
    
    if (studentForm && errorElement) {
        studentForm.addEventListener('submit', async (evt) => {
            evt.preventDefault();
            errorElement.style.display = 'none';
            
            try {
                const formData = new FormData(evt.target);
                const response = await fetch('/teacher/api/students/add/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken(),
                    },
                    body: formData
                });

                const data = await response.json();
                
                if (!response.ok) {
                    const errorMsg = data.error || data.message || 'Ошибка сервера';
                    throw new Error(errorMsg);
                }
                
                addStudentToList(data);
                closeModal();
                
            } catch (error) {
                errorElement.textContent = error.message;
                errorElement.style.display = 'block';
                setTimeout(() => errorElement.style.display = 'none', 5000);
            }
        });
    }

    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    const handleSort = function() {
        const sortField = this.dataset.sort;
        const url = new URL(window.location);
        
        url.searchParams.delete('sort');
        url.searchParams.set('sort', sortField);
        
        window.location = url.toString();
    };

    const initSorting = () => {
        document.querySelectorAll('.sort-header').forEach(header => {
            header.addEventListener('click', handleSort);
        });
    };

    htmx.on('htmx:afterSwap', (evt) => {
        if (evt.detail.target.classList.contains('rating-table')) {
            initSorting();
        }
    });

    initSorting();
});