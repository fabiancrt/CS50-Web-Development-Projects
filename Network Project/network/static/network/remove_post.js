
// here is the js script required to remove posts without refreshing the page and without additional pages similar to all the js functions from before

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.remove-button').forEach(button => {
        button.onclick = () => {
            const postId = button.dataset.postId; 

            fetch(`/remove_post/${postId}`, { 
                method: 'DELETE', 
                headers: {
                    'X-CSRFToken': getCookie('csrftoken') 
                }
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    // actual removal of the post from the dom
                    document.querySelector(`.post[data-post-id="${postId}"]`).remove();
                } else {
                    // (in case of error)
                    alert(result.error);
                }
            })
            .catch(error => console.error('Error:', error)); 
        };
    });
});

// basic get cookie function to get the csrf token
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