# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-03 19:41
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('index', models.IntegerField(primary_key=True, serialize=False)),
                ('departureTime', models.DateTimeField()),
                ('departureTimeAnticipated', models.BooleanField()),
                ('arrivalTime', models.DateTimeField()),
                ('arrivalTimeAnticipated', models.BooleanField()),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departureDate', models.DateField()),
                ('stops', django.contrib.postgres.fields.jsonb.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder)),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('telecode', models.CharField(blank=True, max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('names', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=10), size=None)),
                ('telecode', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('stops', django.contrib.postgres.fields.jsonb.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder)),
            ],
        ),
        migrations.AddField(
            model_name='record',
            name='info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.Train'),
        ),
        migrations.RunSQL("""
            CREATE OR REPLACE VIEW train_stop AS
            SELECT
                info_record.id AS record_id,
                info_id,
                station AS station_id,
                index,
                ("departureDate" + "arrivalTime") AT TIME ZONE 'CCT' AS "arrivalTime",
                "arrivalTimeAnticipated",
                ("departureDate" + "departureTime") AT TIME ZONE 'CCT' AS "departureTime",
                "departureTimeAnticipated"

            FROM info_record, jsonb_to_recordset(stops)
            AS x(
                "index" integer,
                "station" integer,
                "departureTime" interval,
                "departureTimeAnticipated" boolean,
                "arrivalTime" interval,
                "arrivalTimeAnticipated" boolean
            )
        """),
    ]