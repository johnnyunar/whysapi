from django.db import models


class AttributeName(models.Model):
    name = models.CharField(max_length=125)
    code = models.CharField(max_length=125)
    display = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    value = models.CharField(max_length=125)

    def __str__(self):
        return self.value


class Attribute(models.Model):
    name = models.ForeignKey(AttributeName, on_delete=models.CASCADE)
    value = models.ForeignKey(
        AttributeValue, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name.name


class Product(models.Model):
    name = models.CharField(max_length=125)
    description = models.TextField()
    images = models.ManyToManyField("Image", through="ProductImage")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    attributes = models.ManyToManyField(Attribute, through="ProductAttribute")
    published_on = models.DateTimeField(null=True)
    is_published = models.BooleanField()

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product} - {self.attribute}"


class Image(models.Model):
    name = models.CharField(max_length=125, null=True)
    url = models.URLField()

    def __str__(self):
        return f"Image at {self.url}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    name = models.CharField(max_length=125)

    def __str__(self):
        return f"Image of {self.product}"


class Catalog(models.Model):
    name = models.CharField(max_length=125)
    image = models.ForeignKey(Image, null=True, on_delete=models.SET_NULL)
    products = models.ManyToManyField(Product)
    attributes = models.ManyToManyField(Attribute)

    def __str__(self):
        return self.name
