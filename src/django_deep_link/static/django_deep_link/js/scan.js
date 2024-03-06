/* global $, django, ace, hljs */
'use strict';

if (!$) {
  $ = django.jQuery;
}

var scans = {
  initHighlights: function () {
    function prettifyJSON(string, indent = 2) {
      var obj = JSON.parse(string);
      return JSON.stringify(obj, null, indent);
    }

    let elems = [];
    let el = document
      .querySelectorAll('div.field-ua_data')[0]
      .querySelectorAll('div.readonly')[0];

    // el.innerHTML = "<pre>" + prettifyJSON(el.innerHTML) + "</pre>";

    el.style.padding = '6px';
    elems.push(el);

    el = document
      .querySelectorAll('div.field-ip_data')[0]
      .querySelectorAll('div.readonly')[0];
    el.style.padding = '6px';
    elems.push(el);

    el = document
      .querySelectorAll('div.field-query_data')[0]
      .querySelectorAll('div.readonly')[0];
    el.style.padding = '6px';
    elems.push(el);

    elems.forEach((el) => {
      hljs.highlightElement(el);
    });
  },
  changeForm: function () {
    scans.initHighlights();
  },
};

// (function($) {

//     if (document.body.classList.contains('change-form')) {
//         // HACK: Why do we need a timeout?
//         setTimeout(function() {
//             scans.initHighlights();
//         }, 100);
//     }

// })(django.jQuery);

document.addEventListener('DOMContentLoaded', (e) => {
  // if (document.body.classList.contains('change-form')) {
  if (document.body.matches('.model-visit.change-form')) {
    scans.changeForm();
  }
});
