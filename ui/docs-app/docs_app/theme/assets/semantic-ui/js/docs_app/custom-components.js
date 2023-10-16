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
import { MultipleOptionsSearchBar } from "@js/invenio_search_ui/components";
import { i18next } from "@translations/invenio_app_rdm/i18next";
import ReactDOM from "react-dom";
import React from "react";

import "../../less/docs_app/custom-components.less";

/* Expand and collapse navbar  */
const toggleIcon = document.querySelector("#invenio-burger-menu-icon");
const menu = document.querySelector("#invenio-nav");
toggleIcon.addEventListener("click", function () {
  menu.classList.toggle("active");
});

// Burger menu
const burgerIcon = document.querySelector("#invenio-burger-menu-icon");
const closeBurgerIcon = document.querySelector(
  "#invenio-close-burger-menu-icon"
);

const handleBurgerClick = () => {
  burgerIcon.setAttribute("aria-expanded", "true");
  document.querySelector("#invenio-nav").classList.add("active");
  closeBurgerIcon.focus();
  burgerIcon.style.display = "none";
};

const handleBurgerCloseClick = () => {
  burgerIcon.style.display = "block";
  burgerIcon.setAttribute("aria-expanded", "false");
  document.querySelector("#invenio-nav").classList.remove("active");
  burgerIcon.focus();
};

burgerIcon.addEventListener("click", handleBurgerClick);
closeBurgerIcon.addEventListener("click", handleBurgerCloseClick);

const invenioMenu = document.querySelector("#invenio-menu");

invenioMenu.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    handleBurgerCloseClick();
  }
});

const headerSearchbar = document.getElementById("header-search-bar");
if (headerSearchbar) {
  const searchBarOptions = JSON.parse(headerSearchbar.dataset.options);

  ReactDOM.render(
    <MultipleOptionsSearchBar
      options={searchBarOptions}
      placeholder={i18next.t("Search records...")}
    />,
    headerSearchbar
  );
}
