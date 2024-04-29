document.addEventListener('DOMContentLoaded', function() {
    fetch('/titles')
        .then(response => response.json())
        .then(json => {
            const data = json.titles; // JSONオブジェクトからタイトルのリストを取得
            const select = document.getElementById('titlesSelect');
            // 最初の空のオプションを追加
            const initialOption = document.createElement('option');
            initialOption.textContent = "タイトルを選択してください"; // ユーザーに表示するテキスト
            initialOption.value = ""; // 値は空
            select.appendChild(initialOption);

            // タイトルのオプションを追加
            data.forEach(title => {
                const option = document.createElement('option');
                option.value = title;  // タイトルをvalue属性に設定
                option.textContent = title;  // ユーザーにはタイトルのみ表示
                select.appendChild(option);
            });
        });
});

document.getElementById('generateBtn').addEventListener('click', function() {
    const select = document.getElementById('titlesSelect');
    const title = select.value;
    const button = document.getElementById('generateBtn');
    const display = document.getElementById('phraseDisplay');

    if (!title) {
        alert('タイトルを選択してください。');
        return;
    }

    button.disabled = true;  // ボタンを非活性化
    display.textContent = 'loading...';  // ローディングテキストを設定

    fetch(`/generate_phrase?title=${encodeURIComponent(title)}`)
        .then(response => response.json())
        .then(data => {
            display.textContent = data.opinion;  // レスポンスが返ってきたらテキストを更新
            select.selectedIndex = 0;  // セレクトボックスを初期状態にリセット
            button.disabled = false;  // ボタンを再活性化
        })
        .catch(error => {
            console.error('Error:', error);
            display.textContent = 'エラーが発生しました。';  // エラーが発生した場合のテキスト
            button.disabled = false;  // ボタンを再活性化
        });
});
