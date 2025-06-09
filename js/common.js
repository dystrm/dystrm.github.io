function isMobileDevice() {
    return /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
}

// playlist
$(document).on("click", ".playlist_btn", function () {
    $("#playlistContainer").load("modal.html #playlistModal", function () {
        $("#playlistContainer").addClass("show");
        $("body").addClass("scroll-lock");
    });
});

//radio 
$(document).on("click", ".main_btn.ico_radio", function () {
    $("#oneclickRadioContainer").load("modal.html #oneclickRadioModal", function () {
        $("#oneclickRadioContainer").addClass("show");
        $("body").addClass("scroll-lock");

        // 모바일 여부에 따라 pc_txt 처리
        if (isMobileDevice()) {
            $(".pc_txt").hide();
        } else {
            $(".pc_txt").show();
        }
    });
});


$(document).on("click", ".main_btn.ico_click", function () {
    if (isMobileDevice()) {
        // 모바일인 경우
        $("#oneclickMOContainer").load("modal.html #oneclickMOModal", function () {
            $("#oneclickMOContainer").addClass("show");
            $("body").addClass("scroll-lock");
        });
    } else {
        // PC인 경우
        $("#oneclickPCContainer").load("modal.html #oneclickPCModal", function () {
            $("#oneclickPCContainer").addClass("show");
            $("body").addClass("scroll-lock");
        });
    }
});

$(document).on("click", ".oneclick_btn", function () {
    if (isMobileDevice()) {
        // 모바일인 경우
        $("#oneclickMOContainer").load("modal.html #oneclickMOModal", function () {
            $("#oneclickMOContainer").addClass("show");
            $("body").addClass("scroll-lock");
        });
    } else {
        // PC인 경우
        $("#oneclickPCContainer").load("modal.html #oneclickPCModal", function () {
            $("#oneclickPCContainer").addClass("show");
            $("body").addClass("scroll-lock");
        });
    }
});

// modal close
$(document).on("click", ".modal_close_btn", function () {
    $(".modal").removeClass("show").empty();
    $("body").removeClass("scroll-lock");
});

fetch("/js/data/last_update.json")
  .then(res => res.json())
  .then(data => {
    const el = document.querySelector('.footer_wrapper p:last-child');
    if (el && data.last_updated) {
      el.textContent = 'Last Update : ' + data.last_updated;
    }
  })
  .catch(err => {
    console.error("업데이트 시간 불러오기 실패:", err);
  });

//cash
$(document).ready(function () {
    const melonLink = $(".main_btn.ico_coin");

    if (isMobileDevice()) {
        melonLink.attr("href", "https://m2.melon.com/buy/meloncash/charge.htm");
    } else {
        melonLink.attr("href", "https://www.melon.com/buy/meloncash/charge.htm");
    }
});

document.addEventListener("keydown", function (e) {
  // F12
  if (e.key === "F12") {
    e.preventDefault();
    return false;
  }
  // Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+U
  if ((e.ctrlKey && e.shiftKey && (e.key === "I" || e.key === "J")) || (e.ctrlKey && e.key === "U")) {
    e.preventDefault();
    return false;
  }
});

setInterval(function () {
  const before = new Date();
  debugger;
  const after = new Date();
  if (after - before > 100) {
    location.reload(); // 콘솔 열면 새로고침
  }
}, 1000);