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

    onMacChange: () => {
        if (document.getElementById('id_mac_app').checked) {
            document.querySelectorAll('.field-mac_uri_scheme')[0].style.display = "block";
            document.querySelectorAll('.field-mac_app_store_url')[0].style.display = "block";
        } else {
            document.querySelectorAll('.field-mac_uri_scheme')[0].style.display = "none";
            document.querySelectorAll('.field-mac_app_store_url')[0].style.display = "none";
        }
    },

    onWindowsChange: () => {
        if (document.getElementById('id_windows_app').checked) {
            document.querySelectorAll('.field-windows_uri_scheme')[0].style.display = "block";
            document.querySelectorAll('.field-windows_app_store_url')[0].style.display = "block";
            document.querySelectorAll('.field-windows_package_name')[0].style.display = "block";
        } else {
            document.querySelectorAll('.field-windows_uri_scheme')[0].style.display = "none";
            document.querySelectorAll('.field-windows_app_store_url')[0].style.display = "none";
            document.querySelectorAll('.field-windows_package_name')[0].style.display = "none";
        }
    },

    changeForm: () => {
        // console.log('App change form');

        app.oniOSChange();
        app.onAndroidChange();
        app.onMacChange();
        app.onWindowsChange();

        document.getElementById('id_ios_app').addEventListener('change', function () {
            app.oniOSChange();
        });

        document.getElementById('id_android_app').addEventListener('change', function () {
            app.onAndroidChange();
        });

        document.getElementById('id_mac_app').addEventListener('change', function () {
            app.onMacChange();
        });

        document.getElementById('id_windows_app').addEventListener('change', function () {
            app.onWindowsChange();
        });
    }
};

document.addEventListener('DOMContentLoaded', (e) => {

    // if (document.body.classList.contains('change-form')) {
    if (document.body.matches('.model-app.change-form')) {
        app.changeForm();
    }

});
