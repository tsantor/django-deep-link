/* global $, django */
'use strict';

if (!$) {
    $ = django.jQuery;
}

var app = {
    oniOSChange: () => {
        if (document.getElementById('id_ios_app').checked) {
            document.querySelectorAll('.field-ios_uri_scheme')[0].style.display = "block";
            document.querySelectorAll('.field-ios_bundle_id')[0].style.display = "block";
            document.querySelectorAll('.field-ios_custom_url')[0].style.display = "block";
            document.querySelectorAll('.field-ios_url')[0].style.display = "none";

        } else {
            document.querySelectorAll('.field-ios_uri_scheme')[0].style.display = "none";
            document.querySelectorAll('.field-ios_bundle_id')[0].style.display = "none";
            document.querySelectorAll('.field-ios_custom_url')[0].style.display = "none";
            document.querySelectorAll('.field-ios_url')[0].style.display = "block";
        }
    },

    onAndroidChange: () => {
        if (document.getElementById('id_android_app').checked) {
            document.querySelectorAll('.field-android_uri_scheme')[0].style.display = "block";
            document.querySelectorAll('.field-android_package_name')[0].style.display = "block";
            document.querySelectorAll('.field-android_custom_url')[0].style.display = "block";
            document.querySelectorAll('.field-android_url')[0].style.display = "none";
        } else {
            document.querySelectorAll('.field-android_uri_scheme')[0].style.display = "none";
            document.querySelectorAll('.field-android_package_name')[0].style.display = "none";
            document.querySelectorAll('.field-android_custom_url')[0].style.display = "none";
            document.querySelectorAll('.field-android_url')[0].style.display = "block";
        }
    },

    changeForm: () => {
        // console.log('App change form');

        app.oniOSChange();
        app.onAndroidChange();

        document.getElementById('id_ios_app').addEventListener('change', function() {
            app.oniOSChange();
        });

        document.getElementById('id_android_app').addEventListener('change', function() {
            app.onAndroidChange();
        });
    }
};

document.addEventListener('DOMContentLoaded', (e) => {

    // if (document.body.classList.contains('change-form')) {
    if (document.body.matches('.model-app.change-form')) {
        app.changeForm();
    }

});
