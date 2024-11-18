/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.Filters = publicWidget.Widget.extend({
    selector: '#abrakadabra',
    events: {
        click: '_onSubmit',
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
       console.log("sdassa")
    },
});
export default publicWidget.registry.Filters;