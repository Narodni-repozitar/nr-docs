import "@less/branding.less";

import $ from "jquery";


/* Burger menu */
const $burgerIcon = $("#invenio-burger-menu-icon");
const $closeBurgerIcon = $("#invenio-close-burger-menu-icon");

const handleBurgerClick = () => {
    $burgerIcon.attr("aria-expanded", true);
    $("#invenio-nav").addClass("active");
    $closeBurgerIcon.trigger("focus");
    $burgerIcon.css("display", "none");
};

const handleBurgerCloseClick = () => {
    $burgerIcon.css("display", "block");
    $burgerIcon.attr("aria-expanded", false);
    $("#invenio-nav").removeClass("active");
    $burgerIcon.trigger("focus");
};

$burgerIcon.on({ click: handleBurgerClick });
$closeBurgerIcon.on({ click: handleBurgerCloseClick });

const $invenioMenu = $("#invenio-menu");

$invenioMenu.on("keydown", (event) => {
    if (event.key === "Escape") {
        handleBurgerCloseClick();
    }
});
