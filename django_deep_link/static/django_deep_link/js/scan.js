/* global $, django, ace, hljs */
'use strict';

if (!$) {
    $ = django.jQuery;
}

var scans = {
    /**
     * aceEditor
     *
     * Turn specific textareas into an ACE editor
     */
    aceEditor: function () {
        ace.config.set('basePath', '/static/js/ace-builds');

        function prettifyJSON(string, indent = 2) {
            var obj = JSON.parse(string);
            return JSON.stringify(obj, null, indent);
        }

        $('textarea[data-editor]').each(function () {
            // Create a div for ace editor
            var textarea = $(this);
            var mode = textarea.data('editor');
            var editDiv = $('<div>', {
                position: 'absolute',
                width: "100%",
                height: textarea.height() + 15
            }).insertBefore(textarea);
            textarea.css('display', 'none');

            var pretty = prettifyJSON(textarea.val());

            // Create ace editor
            var editor = ace.edit(editDiv[0]);
            editor.setAutoScrollEditorIntoView(true);
            editor.renderer.setShowGutter(textarea.data('gutter'));
            editor.renderer.setShowPrintMargin(false);
            editor.getSession().setValue(pretty);
            editor.getSession().setMode("ace/mode/" + mode);
            editor.getSession().setTabSize(2);
            editor.getSession().setUseWrapMode(true);
            editor.setTheme("ace/theme/chrome");

            // copy back to textarea on form submit...
            textarea.closest('form').submit(function () {
                textarea.val(editor.getSession().getValue());
            });
        });
    },
    initHighlights: function () {

        function prettifyJSON(string, indent = 2) {
            var obj = JSON.parse(string);
            return JSON.stringify(obj, null, indent);
        }

        let elems = [];
        let el = document.querySelectorAll('div.field-ua_data')[0].
            querySelectorAll('div.readonly')[0];

        // el.innerHTML = "<pre>" + prettifyJSON(el.innerHTML) + "</pre>";

        el.style.padding = "6px";
        elems.push(el);

        el = document.querySelectorAll('div.field-ip_data')[0].
            querySelectorAll('div.readonly')[0];
        el.style.padding = "6px";
        elems.push(el);

        elems.forEach((el) => {
            hljs.highlightElement(el);
        });
    },
    initAce: function () {
        // document.getElementById('id_ua_data').setAttribute('data-editor', 'json');
        // document.getElementById('id_ua_data').setAttribute('data-gutter', true);
        // document.getElementById('id_ip_data').setAttribute('data-editor', 'json');
        // document.getElementById('id_ip_data').setAttribute('data-gutter', true);
        // scans.aceEditor();
    },
    changeForm: function() {
        // scans.initAce();
        scans.initHighlights();
    }
};


// (function($) {

//     if (document.body.classList.contains('change-form')) {
//         // HACK: Why do we need a timeout?
//         setTimeout(function() {
//             console.log('yo');
//             // scans.initAce();
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
