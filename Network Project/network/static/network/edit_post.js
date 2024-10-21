
// here is the js thea team required for the edit function , as specified it respects the teams specifications: "Using JavaScript, you
// should be able to achieve this without requiring a reload of the entire page."

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.edit-button').forEach(button => {
        button.onclick = () => {
            const postId = button.dataset.postId;
            const postElement = document.querySelector(`.post[data-post-id="${postId}"]`);
            const postContentElement = postElement.querySelector('.post-content');
            const postContent = postContentElement.innerText;
            const textarea = document.createElement('textarea');
            textarea.id = `edit-content-${postId}`;
            textarea.value = postContent;
            textarea.className = 'form-control'; 
            const saveButton = document.createElement('button');
            saveButton.className = 'btn btn-primary mt-2'; 
            saveButton.dataset.postId = postId;
            saveButton.innerText = 'Save';
            postContentElement.replaceWith(textarea);
            button.replaceWith(saveButton);
            saveButton.onclick = () => {
                const newContent = textarea.value;
                fetch(`/edit_post/${postId}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        content: newContent
                    }),
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                .then(response => response.json())
                .then(result => {
                    if (result.content) {
                        const updatedContentElement = document.createElement('span');
                        updatedContentElement.className = 'post-content';
                        updatedContentElement.innerText = result.content;
                        textarea.replaceWith(updatedContentElement);
                        saveButton.replaceWith(button);
                    } else {
                        alert("The post can't be empty.");
                    }
                });
            };
        };
    });
});

//basic cookie function i used across all my other js files for the csrf token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}