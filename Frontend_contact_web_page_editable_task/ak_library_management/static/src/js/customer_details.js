/** @odoo-module */

import { rpc } from '@web/core/network/rpc';
import publicWidget from '@web/legacy/js/public/public_widget';

publicWidget.registry.SaveCustomerDetails = publicWidget.Widget.extend({
    selector: '.save_customer',
    events: {
        'click .onEditCustomer': '_onEditDetailsCustomer',
        'click .onSaveCustomer': '_onSaveDetailsCustomer',
    },
    _onEditDetailsCustomer: function () {
        const inputs = this.$('input[type="text"], input[type="email"], input[type="tel"]');
        inputs.prop('readonly', false);
        this.$('.onEditCustomer').hide();
        this.$('.onSaveCustomer').show();
    },
    _onSaveDetailsCustomer: async function (event) {
        event.preventDefault();
        const customerId = parseInt(this.$('.customer-id').val());
        const data = {
            name: this.$('#name').val(),
            email: this.$('#email').val(),
            website: this.$('#website').val(),
            phone: this.$('#phone').val(),
            vat: this.$('#vat').val(),
            mobile: this.$('#mobile').val(),
        };

        if (!data.name || !data.email || !data.phone) {
            alert('Please fill in all required fields.');
            return;
        }

        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(data.email)) {
            alert('Please enter a valid email address.');
            return;
        }

        const phonePattern = /^\d{10}$/;
        if (!phonePattern.test(data.phone)) {
            alert('Please enter a valid phone number (10 digits).');
            return;
        }
        try {
            const result = await rpc('/partner/save', {
                partner_id: customerId,
                name: data.name,
                email: data.email,
                website: data.website,
                phone: data.phone,
                vat: data.vat,
                mobile: data.mobile,
            });
            if (result && result.success) {
                const inputs = this.$('input[type="text"], input[type="email"], input[type="tel"]');
                inputs.prop('readonly', true);
                this.$('.onEditCustomer').show();
                this.$('.onSaveCustomer').hide();
                alert('Customer details saved successfully!');
            } else {
                alert(`Error: ${result.error || 'An unknown error occurred.'}`);
            }
        } catch (error) {
            console.error('Error saving customer details:', error);
            alert('You must be sign in to edit the details');
        }
    }
});
