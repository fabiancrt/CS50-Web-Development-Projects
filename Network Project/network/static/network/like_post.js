
// here is the like post feature that the team required that does just this as requested :  "like count displayed on the page,
// without requiring a reload of the entire page."

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.like-button').forEach(button => {
        const postId = button.dataset.postId;

        fetch(`/post/${postId}/like/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(result => {
            if (result.is_liked) {
                const heartIcon = button.querySelector('i');
                heartIcon.classList.remove('fa-heart-o');
                heartIcon.classList.add('fa-heart');
            }
        })
        .catch(error => console.error('error fetching like:', error));

        button.onclick = () => {
            fetch(`/post/${postId}/like/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('network response not ok');
                }
                return response.json();
            })
            .then(result => {
                if (result.success) {
                    const likeCountElement = button.querySelector('.like-count');
                    const heartIcon = button.querySelector('i');
                    likeCountElement.innerText = result.likes_count;
                    if (result.is_liked) {
                        heartIcon.classList.remove('fa-heart-o');
                        heartIcon.classList.add('fa-heart');
                    } else {
                        heartIcon.classList.remove('fa-heart');
                        heartIcon.classList.add('fa-heart-o');
                    }
                } else {
                    alert(result.error);
                }
            })
            .catch(error => console.error('Error:', error));
        };
    });
});


//basic cookie function for the csrf token
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