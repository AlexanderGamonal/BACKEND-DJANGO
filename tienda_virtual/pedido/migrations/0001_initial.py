# Generated by Django 4.2.3 on 2023-08-05 05:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('producto', '0004_alter_review_producto'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calle', models.CharField(default='', max_length=500)),
                ('distrito', models.CharField(default='', max_length=100)),
                ('departamento', models.CharField(default='', max_length=100)),
                ('codigo_postal', models.CharField(default='', max_length=100)),
                ('telefono', models.CharField(default='', max_length=100)),
                ('pais', models.CharField(default='', max_length=100)),
                ('monto_total', models.IntegerField(default=0)),
                ('estado_pago', models.CharField(choices=[('PAGADO', 'Pagado'), ('SIN PAGAR', 'Sinpagar')], default='SIN PAGAR', max_length=20)),
                ('estado', models.CharField(choices=[('En Proceso', 'Enproceso'), ('Enviado', 'Enviado'), ('Entregado', 'Entregado')], default='En Proceso', max_length=50)),
                ('modo_pago', models.CharField(choices=[('COD', 'Cod'), ('TARJETA', 'Tarjeta')], default='COD', max_length=50)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ArticuloPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='', max_length=200)),
                ('cantidad', models.IntegerField(default=1)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=7)),
                ('pedido', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='articulospedidos', to='pedido.pedido')),
                ('producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='producto.producto')),
            ],
        ),
    ]