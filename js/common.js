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

const now = new Date();
const formatted = `${now.getFullYear()}.${(now.getMonth()+1).toString().padStart(2, '0')}.${now.getDate().toString().padStart(2, '0')} ${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
document.addEventListener("DOMContentLoaded", () => {
    const el = document.querySelector('.footer_wrapper p:last-child');
    if (el) el.textContent = 'Last Update : ' + formatted;
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
