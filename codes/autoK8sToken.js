// ==UserScript==
// @name         AutoK8sToken
// @namespace    http://tampermonkey.net/
// @version      0.1
// @author       MoYi
// @match        k8s.bb.local
// @run-at       document-idle
// ==/UserScript==

(function () {
    'use strict';
    var token = "";
    setTimeout(function () {
        console.log(document.getElementById("mat-radio-2-input").checked)
        let inputToken = document.getElementsByName("token")[0];
        var event = new Event('change');
        inputToken.value = token
        inputToken.dispatchEvent(event)
        document.getElementsByClassName("mat-ripple mat-button-ripple")[0].click()
    }, 1000)
}())
