/* @odoo-module */

import publicWidget from '@web/legacy/js/public/public_widget';
import { rpc } from "@web/core/network/rpc";
import { cartHandlerMixin } from '@website_sale/js/website_sale_utils';
import { WebsiteSale } from '@website_sale/js/website_sale';
publicWidget.registry.ShopPageQuickAddToCart = WebsiteSale.extend(cartHandlerMixin, {
    selector: '.oe_website_sale',
    events: {
        'click .js_add_cart_json': '_onClickQuickAddToCart',
    },

    _onClickQuickAddToCart: function (ev) {
        ev.preventDefault();
        const $button = $(ev.currentTarget);
        const productId = $button.data('product-id');
        rpc("/shop/product/is_add_to_cart_allowed", {
            product_id: productId,
        }).then((isAllowed) => {
            if (isAllowed) {
                this.addToCart({ product_id: productId, add_qty: 1 });
            } else {
                alert('This product cannot be added to the cart.');
            }
        });
    },
});
