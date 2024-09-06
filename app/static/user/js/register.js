// register.js
//廃止
/*
document.addEventListener("DOMContentLoaded", function() {
    const main = document.getElementById("main");
    let lines = document.querySelectorAll('.line');
    let memoryCheckTarget = 16384;
    let memoryIncrement = Math.ceil(memoryCheckTarget / (5 * 10));
    let progressBar = document.getElementById('progress');
    let memory = document.getElementById('memory');
    let percent = document.getElementById('percent');
    let memoryValue = 0;
    let progressValue = 0;
    let delay = 500;
    let removalInterval = 50;
    let systemCheckIndex = 1;
    let memoryIndex = 2;
    let networkAdapter = 4;
    let progressIndex = 6;
    let OSRun = 10;
    function deleteLine(lineIndex) {
        if (lineIndex >= lines.length) {
            main.style.display = "block";
            return;
        }
        let line = lines[lineIndex];
        line.style.display = 'none';
        setTimeout(() => deleteLine(lineIndex + 1), removalInterval);
    }

    function showLine(line, index) {
        return new Promise((resolve) => {
            setTimeout(() => {
                line.style.display = 'block';
                if(index === systemCheckIndex){
                    let systemCheckTime = 8;
                    let i = 0;
                    let systemCheck = document.getElementById("system_check");
                    let systemCheckInterval = setInterval(() => {
                        i += 1;
                        if(systemCheckTime < i) {
                            systemCheck.innerText = `Passed`;
                            clearInterval(500);
                            resolve();
                        }
                    }, 100);
                }
                if (index === memoryIndex) {
                    let memoryInterval = setInterval(() => {
                        memoryValue += memoryIncrement;
                        if (memoryValue >= memoryCheckTarget) {
                            memoryValue = memoryCheckTarget;
                            clearInterval(memoryInterval);
                            line.innerHTML = `Memory Check: ${memoryValue} MB OK`;
                            resolve();
                        } else {
                            memory.innerText = `${memoryValue} MB`;
                        }
                    }, 50);
                } else if (index === progressIndex) {
                    let progressInterval = setInterval(() => {
                        progressValue += 1;
                        let filledBlocks = Math.floor(progressValue / 10);
                        let emptyBlocks = 10 - filledBlocks;
                        let progressBarContent = '[' + '███'.repeat(filledBlocks) + '---'.repeat(emptyBlocks) + ']';
                        progressBar.innerHTML = progressBarContent;
                        percent.innerText = `${progressValue}%`;
                        if (progressValue >= 100) {
                            progressBar.innerHTML = `[██████████████████████████████]`;
                            percent.innerText = '100%';
                            clearInterval(progressInterval);
                            resolve();
                        }
                    }, 10);
                } else {
                    resolve();
                }
            }, delay);
            if (index === memoryIndex || index === progressIndex) {
                delay = 1000;
            } else if (index === OSRun || index === systemCheckIndex) {
                delay = 2000;
            } else {
                delay = Math.random() * 500 + 200;
            }
        });
    }

    async function runSequence() {
        for (let i = 0; i < lines.length; i++) {
            await showLine(lines[i], i);
        }
        setTimeout(() => deleteLine(0), 1000);  // シーケンスの最後に実行
    }

    runSequence();
    console.debug(lines.length);
    //mainでの動作プログム
    const usernameInput = document.querySelector("#usernameDiv input");
    const emailDiv = document.getElementById("emailDiv");
    const passwordDiv = document.getElementById("passwordDiv");
    const confirmPasswordDiv = document.getElementById("confirmPasswordDiv");
    const submitDiv = document.getElementById("submitDiv");
    // 初期状態ではusernameの入力にフォーカス
    usernameInput.focus();

    // Enterキーを押したときの挙動を設定
    usernameInput.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            // usernameの次にemailフィールドを表示
            emailDiv.classList.remove("hidden");
            emailDiv.querySelector("input").focus();
        }
    });

    document.querySelector("#emailDiv input").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            // emailの次にpasswordフィールドを表示
            passwordDiv.classList.remove("hidden");
            passwordDiv.querySelector("input").focus();
        }
    });

    document.querySelector("#passwordDiv input").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            // passwordの次にconfirm_passwordフィールドを表示
            confirmPasswordDiv.classList.remove("hidden");
            confirmPasswordDiv.querySelector("input").focus();
        }
    });

    document.querySelector("#confirmPasswordDiv input").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            // 全てのフィールドが入力されたらsubmitボタンを表示
            submitDiv.classList.remove("hidden");
            submitDiv.querySelector("input").focus();
        }
    });

    //サウンド
    document.getElementById('submitDiv').addEventListener('click', function() {
            // フォーム内のエラーメッセージを確認
        let errorElements = document.querySelectorAll('span[style*="color: red"]');
        let hasErrors = errorElements.length > 0;

        if (hasErrors) {
            // エラーがある場合、エラー音を再生
            document.getElementById('error-sound').play();
        } else {
            // エラーがない場合、ブート音を再生
            document.getElementById('deep-sound').play();
        }
    });
});
*/
