document.addEventListener('DOMContentLoaded', () => {
    const handleSort = (e) => {
        const sortField = e.target.dataset.sort;
        const url = new URL(window.location);
        
        if(url.searchParams.get('sort') === sortField) {
            url.searchParams.set('sort', `-${sortField}`);
        } else {
            url.searchParams.set('sort', sortField);
        }
        
        fetch(url)
            .then(response => response.text())
            .then(html => {
                document.querySelector('.rating-table').innerHTML = 
                    new DOMParser().parseFromString(html, 'text/html')
                    .querySelector('.rating-table').innerHTML;
            });
    };

    const initSorting = () => {
        document.querySelectorAll('.sort-header').forEach(header => {
            header.addEventListener('click', handleSort);
            const currentSort = new URL(window.location).searchParams.get('sort');
            if(currentSort === header.dataset.sort) {
                header.classList.add('sorted-asc');
            } else if(currentSort === `-${header.dataset.sort}`) {
                header.classList.add('sorted-desc');
            }
        });
    };

    document.body.addEventListener('htmx:afterSwap', initSorting);
    initSorting();
});