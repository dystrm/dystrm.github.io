   document.addEventListener('DOMContentLoaded', function () {
       var apiKey = 'AIzaSyBlutTPaSd_dQRXEHXfyKs-SkbGjYfaf-c';
       var apiUrl = 'https://www.googleapis.com/youtube/v3/videos';
       var videoId = 'zpPFHclAOoM';

       fetch(`${apiUrl}?part=statistics&id=${videoId}&key=${apiKey}`)
           .then(response => response.json())
           .then(data => {
               const stats = data.items[0].statistics;
               const viewCount = stats.viewCount;
               const likeCount = stats.likeCount;

               document.querySelector('.count.view').textContent = formatNumber(viewCount);
               document.querySelector('.count.like').textContent = formatNumber(likeCount);
           })
           .catch(error => {
               console.error('Error fetching YouTube data:', error);
           });

       function formatNumber(num) {
           const n = parseInt(num, 10);
           if (n >= 100000000) return (n / 100000000).toFixed(1) + '억';
           if (n >= 10000) return (n / 10000).toFixed(1) + '만';
           if (n >= 1000) return (n / 1000).toFixed(1) + '천';
           return n.toLocaleString();
       }

       const playlist = document.querySelector('.playlist');
       if (playlist) {
           playlist.addEventListener('click', function () {
               window.location.href = './guide.html';
           });
       }
   });