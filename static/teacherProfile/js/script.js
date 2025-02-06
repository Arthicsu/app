function showAddForm() {
    document.getElementById('addModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('addModal').style.display = 'none';
}

document.getElementById('studentForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const response = await fetch('/api/add-student/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
        },
        body: formData
    });

    if (response.ok) {
        const data = await response.json();
        addStudentToList(data);
        closeModal();
    }
});

function addStudentToList(student) {
    const list = document.getElementById('students-list');
    const item = document.createElement('div');
    item.className = 'student-item';
    item.innerHTML = `
        <span>${list.children.length + 1}. ${student.full_name}</span>
    `;
    list.appendChild(item);
}

// Управление группами
async function addGroup() {
    const groupId = document.getElementById('availableGroups').value;
    const response = await fetch(`/api/groups/${groupId}/add/`, {
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

// Обновление URL при удалении группы
async function removeGroup(event, groupId) {
    event.stopPropagation();
    const response = await fetch(`/api/groups/${groupId}/remove/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value }
    });
    
    if (response.ok) {
        const params = new URLSearchParams(window.location.search);
        if (params.get('group') == groupId) {
            params.delete('group');
            window.location.search = params.toString();
        } else {
            window.location.reload();
        }
    }
}

// Удаление студента
async function deleteStudent(studentId) {
    const response = await fetch(`/api/students/${studentId}/delete/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
    });
    
    if (response.ok) {
        document.querySelector(`.student-item[data-id="${studentId}"]`).remove();
    }
}

