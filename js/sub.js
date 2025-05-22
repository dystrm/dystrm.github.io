$(document).ready(function () {
    // ✅ 초기화: 각 메뉴에서 첫 번째 요소 활성화
    $('.menu_depth_01 ul li').eq(0).addClass('active');
    $('.menu_depth_02 ul').eq(0).addClass('show').find('li').eq(0).addClass('active');
    $('.sub_contents .category_box').eq(0).addClass('show').find('.box').eq(0).addClass('show').find('ul li').eq(1).addClass('active'); // li[1]은 tit 제외
    $('.sub_contents .category_box').eq(0).find('.box').eq(0).find('.image_box > div').eq(0).addClass('show');

    // 1단계 메뉴 클릭: menu_depth_01 > li
    $('.menu_depth_01 ul li').click(function () {
        const index = $(this).index();

        $('.menu_depth_01 ul li').removeClass('active');
        $(this).addClass('active');

        $('.menu_depth_02 ul').removeClass('show').eq(index).addClass('show').find('li').removeClass('active').eq(0).addClass('active');

        $('.sub_contents .category_box').removeClass('show').eq(index).addClass('show');
        const $targetCategory = $('.sub_contents .category_box').eq(index);
        $targetCategory.find('.box').removeClass('show').eq(0).addClass('show').find('ul li').removeClass('active').eq(1).addClass('active');
        $targetCategory.find('.box').eq(0).find('.image_box > div').removeClass('show').eq(0).addClass('show');
    });

    // 2단계 메뉴 클릭: menu_depth_02 > ul > li
    $('.menu_depth_02 ul li').click(function () {
        const $this = $(this);
        const index = $this.index();

        $this.siblings().removeClass('active');
        $this.addClass('active');

        const $categoryBox = $('.sub_contents .category_box.show');
        $categoryBox.find('.box').removeClass('show').eq(index).addClass('show')
            .find('ul li').removeClass('active').eq(1).addClass('active');
        $categoryBox.find('.box').eq(index).find('.image_box > div').removeClass('show').eq(0).addClass('show');
    });

    // 3단계 세부 항목 클릭: category_box > box > ul > li (tit 제외)
    $('.category_box .box ul li').click(function () {
        if ($(this).hasClass('tit')) return;

        const index = $(this).index() - 1; // tit 제외
        const $box = $(this).closest('.box');

        $box.find('ul li').removeClass('active');
        $(this).addClass('active');

        $box.find('.image_box > div').removeClass('show').eq(index).addClass('show');
    });
});
