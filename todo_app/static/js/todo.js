// Background changing functionality
function changeBackground(bgClass, event) {
    // Remove all background classes
    document.body.className = '';
    
    // Add the selected background class
    document.body.classList.add(bgClass);
    
    // Update active state on selector buttons
    document.querySelectorAll('.bg-option').forEach(option => {
        option.classList.remove('active');
    });
    
    // Add active class to clicked option
    if (event) {
        event.target.classList.add('active');
    } else {
        // This is for page load, so we find the correct thumb
        const thumb = document.querySelector(`.${bgClass}-thumb`);
        if (thumb) {
            thumb.classList.add('active');
        }
    }
    
    // Save preference to localStorage
    localStorage.setItem('selectedBackground', bgClass);
}

// Load saved background on page load
window.addEventListener('load', function() {
    const savedBg = localStorage.getItem('selectedBackground');
    if (savedBg) {
        changeBackground(savedBg);
    }
});

// Task functionality
document.addEventListener('DOMContentLoaded', function() {
    const taskList = document.getElementById('task-list');

    if (!taskList) return;

    // Handle task interactions
    taskList.addEventListener('click', function(e) {
        // Toggle complete
        if (e.target.classList.contains('checkbox')) {
            const li = e.target.closest('li');
            const taskId = li.dataset.id;

            if (!window.toggleCompleteUrl || !window.csrfToken) {
                console.error('Required URLs or CSRF token not available');
                return;
            }

            fetch(window.toggleCompleteUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': window.csrfToken
                },
                body: JSON.stringify({id: taskId})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Toggle the check icon and line-through
                    if (data.completed) {
                        e.target.textContent = '✔️';
                        li.querySelector('.task-text').classList.add('completed');
                    } else {
                        e.target.textContent = '☐';
                        li.querySelector('.task-text').classList.remove('completed');
                    }
                }
            })
            .catch(error => {
                console.error('Error toggling task completion:', error);
            });
        }

        // Delete task
        if (e.target.classList.contains('delete-btn')) {
            const li = e.target.closest('li');
            const taskId = li.dataset.id;

            if (!window.deleteTaskUrl || !window.csrfToken) {
                console.error('Required URLs or CSRF token not available');
                return;
            }

            fetch(window.deleteTaskUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': window.csrfToken
                },
                body: JSON.stringify({id: taskId})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    li.remove(); // Remove the task from DOM instantly
                }
            })
            .catch(error => {
                console.error('Error deleting task:', error);
            });
        }
    });
});