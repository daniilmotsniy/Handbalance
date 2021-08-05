var button = $ipsp.get('button');

button.setMerchantId(1396424);
button.setAmount(9.99, 'USD', true);
button.setResponseUrl('http://ec2-18-119-160-153.us-east-2.compute.amazonaws.com/buy');
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