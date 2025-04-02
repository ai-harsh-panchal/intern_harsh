/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.CustomerFetch = publicWidget.Widget.extend({
    selector: '.customer-fetch',
    events: {
        'click .fetch-button': '_onFetchCustomer'
    },

    _onFetchCustomer: function(ev) {
        const email = this.$('#InputEmail').val();
        if (email) {
            rpc("/fetch_customer", {'email': email}).then(
                (data) => {
                    this.$('#InputName').val(data.name || '');
                    this.$('#InputAddress').val(data.address || '');
                    this.$('#InputPhone').val(data.phone || '');
                }
            ).catch((error) => {
                console.error('Error fetching customer:', error);
            });
        } else {
            this.$('#InputName').val('');
            this.$('#InputAddress').val('');
            this.$('#InputPhone').val('');
        }
    }
});
