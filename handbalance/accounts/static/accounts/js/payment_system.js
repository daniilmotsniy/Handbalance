var button = $ipsp.get('button');

button.setMerchantId(1396424);
button.setAmount(9.99, 'USD', true);
button.setResponseUrl('/account');
button.setHost('pay.fondy.eu');
button.addField({
    label: 'Your email',
    name: 'email',
    required: true
});

button.addField({
    label: 'Good description',
    name: 'description',
    value: 'Handbalance course',
    readonly: true
});