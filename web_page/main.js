const API_URL = '/api/pet';

let currentPage = 1;
let pageSize = 5;
let currentCategory = '';
let currentSearch = '';

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('searchBtn').onclick = () => {
        currentSearch = document.getElementById('searchInput').value.trim();
        currentPage = 1;
        loadPets();
    };
    document.getElementById('categoryFilter').onchange = () => {
        currentCategory = document.getElementById('categoryFilter').value;
        currentPage = 1;
        loadPets();
    };
    document.getElementById('pageSize').onchange = () => {
        pageSize = parseInt(document.getElementById('pageSize').value, 10);
        currentPage = 1;
        loadPets();
    };
    loadPets();
});

async function loadPets() {
    let url = `${API_URL}?page=${currentPage}&size=${pageSize}`;
    if (currentCategory) url += `&filter=${encodeURIComponent(currentCategory)}`;
    if (currentSearch) url += `&search=${encodeURIComponent(currentSearch)}`;

    const res = await fetch(url);
    const data = await res.json();

    renderPetList(data.data || []);
    renderPagination(data.total || 0, data.page || 1, data.size || pageSize);

    // Render category filter options (lấy từ data)
    renderCategoryOptions(data.data || []);
}

function renderPetList(pets) {
    const list = document.getElementById('petList');
    list.innerHTML = '';
    if (pets.length === 0) {
        list.innerHTML = '<p>Không có thú cưng nào phù hợp.</p>';
        return;
    }
    pets.forEach(pet => {
        const card = document.createElement('div');
        card.className = 'pet-card';
        card.innerHTML = `
            <div class="pet-image">
                <img src="${pet.image_url}" alt="${pet.subject}">
            </div>
            <div class="pet-info">
                <div class="pet-title">${pet.subject}</div>
                <div class="pet-desc">${pet.param_value} • ${pet.category_name}</div>
                <div class="pet-price">${pet.price_string}</div>
                <div class="pet-meta">
                    <span class="pet-location">${pet.area_name}</span>
                    <span class="pet-label">Tin ưu tiên</span>
                    <span style="margin-left:8px;">${pet.date_string}</span>
                </div>
                <div class="pet-shop">
                    <span class="shop-icon">🐾</span>
                    <span class="shop-name">${pet.seller_name}</span>
                    <span class="shop-rating">${pet.average_rating} <span class="star">★</span></span>
                    <span class="shop-sold">${pet.sold_ads} đã bán</span>
                </div>
            </div>
            <div class="pet-fav">
                <span class="fav-icon">♡</span>
            </div>
        `;
        list.appendChild(card);
    });
}

function renderPagination(total, page, size) {
    const totalPages = Math.ceil(total / size);
    const pag = document.getElementById('pagination');
    pag.innerHTML = '';
    if (totalPages <= 1) return;

    // Nút prev
    const prevBtn = document.createElement('button');
    prevBtn.textContent = '<';
    prevBtn.disabled = page === 1;
    prevBtn.onclick = () => {
        if (currentPage > 1) {
            currentPage--;
            loadPets();
        }
    };
    pag.appendChild(prevBtn);

    // Các nút số trang
    for (let i = 1; i <= totalPages; i++) {
        const btn = document.createElement('button');
        btn.textContent = i;
        if (i === page) btn.className = 'active';
        btn.onclick = () => {
            currentPage = i;
            loadPets();
        };
        pag.appendChild(btn);
    }

    // Nút next
    const nextBtn = document.createElement('button');
    nextBtn.textContent = '>';
    nextBtn.disabled = page === totalPages;
    nextBtn.onclick = () => {
        if (currentPage < totalPages) {
            currentPage++;
            loadPets();
        }
    };
    pag.appendChild(nextBtn);
}

function renderCategoryOptions(pets) {
    const select = document.getElementById('categoryFilter');
    // Lấy tất cả category_name duy nhất từ pets
    const categories = new Set(pets.map(p => p.category_name).filter(Boolean));
    // Nếu đã có option thì không render lại nữa
    if (select.options.length > 1) return;
    select.innerHTML = '<option value="">Tất cả danh mục</option>';
    categories.forEach(cat => {
        const opt = document.createElement('option');
        opt.value = cat;
        opt.textContent = cat;
        select.appendChild(opt);
    });
}   