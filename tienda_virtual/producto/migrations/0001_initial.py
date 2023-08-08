# Generated by Django 4.2.3 on 2023-07-29 22:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, default='', max_length=100, verbose_name='Nombre')),
                ('descripcion', models.TextField(max_length=200)),
                ('precio', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('marca', models.CharField(default='', max_length=200)),
                ('categoria', models.CharField(choices=[('Computadoras', 'Computadoras'), ('Laptops', 'Laptops'), ('Celulares', 'Celulares'), ('Tablets', 'Tablets')], max_length=30)),
                ('disponible', models.PositiveIntegerField(default=0)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]