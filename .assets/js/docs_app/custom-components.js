/*
This is the registration file for custom components. The components should not be included here,
but only referenced. The sample component below can be used to start up working on your own custom
component.
*/
/*

In the sample-component.js you can define your own javascript functions etc for your custom component.
Then import the file here

import "./sample-component.js"
*/

// This file will import the css templates for your custom components
import $ from "jquery";
import { MultipleOptionsSearchBar } from "@js/invenio_search_ui/components";
import { i18next } from "@translations/invenio_app_rdm/i18next";
import ReactDOM from "react-dom";
import React from "react";

import "../../less/docs_app/custom-components.less"



/* Expand and collapse navbar  */
const toggleIcon = $("#invenio-burger-menu-icon");
const menu = $("#invenio-nav");

toggleIcon.on("click", function () {
    menu.toggleClass("active");
});

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
