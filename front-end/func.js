let btn = document.querySelector('.more_btn);
let wrap = document.querySelector('.content');

btn.onclick = function (e) {
    let text = e.target.innerText === '展开' ? '收起' : '展开';
    e.target.innerText = text;
    if (text === '收起') {
        wrap.classList.add('open');
    } else {
        wrap.classList.remove('open');
    }
};