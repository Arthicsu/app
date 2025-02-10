function showAddForm() {
    document.getElementById('addModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('addModal').style.display = 'none';
}

async function addGroup() {
    const groupId = document.getElementById('availableGroups').value;
    const response = await fetch(`/teacher/api/groups/${groupId}/add/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
    });
    
    if (response.ok) {
        window.location.reload();
    }
}

function updateGroups() {
    const faculty = document.getElementById('facultySelect').value;
    const course = document.getElementById('courseSelect').value;
    const params = new URLSearchParams(window.location.search);
    
    params.set('faculty', faculty);
    params.set('course', course);
    window.location.search = params.toString();
}

document.addEventListener('DOMContentLoaded', () => {
    // Обработчик выбора группы
    document.querySelectorAll('.group-tab').forEach(tab => {
        tab.addEventListener('click', function() {
            const groupId = this.dataset.groupId;
            const url = new URL(window.location);
            
            if (this.classList.contains('active')) {
                url.searchParams.delete('group');
            } else {
                url.searchParams.set('group', groupId);
            }
            
            window.location.href = url.toString();
        });
    });

    // Обновляем активную группу при загрузке
    const params = new URLSearchParams(window.location.search);
    const activeGroupId = params.get('group');
    if (activeGroupId) {
        const activeTab = document.querySelector(`.group-tab[data-group-id="${activeGroupId}"]`);
        if (activeTab) activeTab.classList.add('active');
    }
});

// Модифицированная функция удаления группы
async function removeGroup(event, groupId) {
    event.stopPropagation();
    const response = await fetch(`/teacher/api/groups/${groupId}/remove/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value }
    });
    
    if (response.ok) {
        const params = new URLSearchParams(window.location.search);
        const curatedGroups = document.querySelectorAll('.group-tab');
        
        if (params.get('group') == groupId && curatedGroups.length > 0) {
            // Выбираем первую доступную группу после удаления
            const newGroupId = curatedGroups[0].dataset.groupId;
            params.set('group', newGroupId);
        } else if (curatedGroups.length === 0) {
            params.delete('group');
        }
        
        window.location.search = params.toString();
    }
}

async function deleteStudent(studentId) {
    const response = await fetch(`/teacher/api/students/${studentId}/delete/`, { // Добавлен префикс
        method: 'DELETE',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
    });
    
    if (response.ok) {
        document.querySelector(`.student-item[data-id="${studentId}"]`).remove();
    }
}

function addStudentToList(student) {
    const list = document.getElementById('students-list');
    const item = document.createElement('div');
    item.className = 'student-item';
    item.innerHTML = `
        <span>${list.children.length + 1}. ${student.full_name}</span>
    `;
    list.appendChild(item);
}

document.addEventListener('DOMContentLoaded', () => {
    const studentForm = document.getElementById('studentForm');
    const errorElement = document.getElementById('error-message');

    if (studentForm && errorElement) {
        studentForm.addEventListener('submit', async (evt) => {
            evt.preventDefault();
            errorElement.style.display = 'none';
            
            try {
                const formData = new FormData(evt.target);
                const response = await fetch('/teacher/api/students/add/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                    },
                    body: formData
                });

                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Ошибка сервера');
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

    const handleSort = function() {
        const sortField = this.dataset.sort;
        const url = new URL(window.location);
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

