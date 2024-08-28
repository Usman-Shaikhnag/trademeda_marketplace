/** @odoo-module **/

odoo.define('trademeda.Filters', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');  // Make sure this path is correct

    publicWidget.registry.Filters = publicWidget.Widget.extend({
        selector: '#abrakadabra',
        events: {
            'click': '_onSubmit', // Add quotes around the event
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        /**
         * Prevents the user from crazy clicking:
         * Gives the button a loading effect if preventDefault was not already
         * called and modifies the preventDefault function of the event so that the
         * loading effect is removed if preventDefault() is called in a following
         * customization.
         *
         * @private
         * @param {Event} ev
         */
        _onSubmit: function () {
           console.log("Button clicked");
        },
    });

    return publicWidget.registry.Filters;
});