function redirectToDatePage(event) {
    event.preventDefault();
    const dateInput = document.getElementById('date-input').value;
    const formattedDate = dateInput.replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3');
    window.location.href = `/game/${formattedDate}`;
}
// メニューの表示・非表示を切り替える
function toggleMenu() {
    var menuContent = document.getElementById('menuContent');
    menuContent.style.display = menuContent.style.display === 'block' ? 'none' : 'block';
}

// メニュー外をクリックするとメニューを閉じる
document.addEventListener('click', function(event) {
    var menuContent = document.getElementById('menuContent');
    var menuButton = document.querySelector('.menu button');
    if (!menuContent.contains(event.target) && !menuButton.contains(event.target)) {
        menuContent.style.display = 'none';
    }
});

// 過去の検索履歴を保存するためのローカルストレージ機能
const dateInput = document.getElementById('dateInput');
const searchHistory = document.getElementById('searchHistory');
const MAX_HISTORY = 10;  // 最大表示数

function saveSearchHistory(date) {
    let history = JSON.parse(localStorage.getItem('searchHistory')) || [];
    if (!history.includes(date)) {
        history.push(date);
        if (history.length > MAX_HISTORY) {
            history.shift();  // 古い履歴を削除
        }
        localStorage.setItem('searchHistory', JSON.stringify(history));
        updateSearchHistory();
    }
}

function updateSearchHistory() {
    searchHistory.innerHTML = '';
    let history = JSON.parse(localStorage.getItem('searchHistory')) || [];
    history.forEach(date => {
        let option = document.createElement('option');
        option.value = date;
        searchHistory.appendChild(option);
    });
}

function formatDateString(value) {
    if (value.length === 8) {
        return `${value.slice(0, 4)}-${value.slice(4, 6)}-${value.slice(6, 8)}`;
    }
    return value;
}

dateInput.addEventListener('input', (event) => {
    let value = event.target.value.replace(/-/g, '');  // ハイフンを削除
    if (value.length <= 8) {
        event.target.value = formatDateString(value);
    }
});

dateInput.addEventListener('blur', () => {
    saveSearchHistory(dateInput.value);
});

document.addEventListener('DOMContentLoaded', updateSearchHistory);