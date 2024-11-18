/** @odoo-module **/
import publicWidget from '@web/legacy/js/public/public_widget';
import dom from '@web/legacy/js/core/dom';


publicWidget.registry.Filters = publicWidget.Widget.extend({
    selector: '#abrakadabra',
    events: {
        'click': '_onSubmit', // Specify the event and the handler
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * Handles the click event on the button with ID 'abrakadabra'.
     *
     * @private
     * @param {Event} ev
     */
    _onSubmit: function () {
        console.log("Button clicked");
    },
});