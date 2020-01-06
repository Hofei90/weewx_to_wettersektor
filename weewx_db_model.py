from peewee import *

database = Proxy()


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Archive(BaseModel):
    et = FloatField(column_name='ET', null=True)
    uv = FloatField(column_name='UV', null=True)
    altimeter = FloatField(null=True)
    barometer = FloatField(null=True)
    cons_battery_voltage = FloatField(column_name='consBatteryVoltage', null=True)
    date_time = AutoField(column_name='dateTime')
    dewpoint = FloatField(null=True)
    extra_humid1 = FloatField(column_name='extraHumid1', null=True)
    extra_humid2 = FloatField(column_name='extraHumid2', null=True)
    extra_temp1 = FloatField(column_name='extraTemp1', null=True)
    extra_temp2 = FloatField(column_name='extraTemp2', null=True)
    extra_temp3 = FloatField(column_name='extraTemp3', null=True)
    hail = FloatField(null=True)
    hail_rate = FloatField(column_name='hailRate', null=True)
    heatindex = FloatField(null=True)
    heating_temp = FloatField(column_name='heatingTemp', null=True)
    heating_voltage = FloatField(column_name='heatingVoltage', null=True)
    in_humidity = FloatField(column_name='inHumidity', null=True)
    in_temp = FloatField(column_name='inTemp', null=True)
    in_temp_battery_status = FloatField(column_name='inTempBatteryStatus', null=True)
    interval = IntegerField()
    leaf_temp1 = FloatField(column_name='leafTemp1', null=True)
    leaf_temp2 = FloatField(column_name='leafTemp2', null=True)
    leaf_wet1 = FloatField(column_name='leafWet1', null=True)
    leaf_wet2 = FloatField(column_name='leafWet2', null=True)
    out_humidity = FloatField(column_name='outHumidity', null=True)
    out_temp = FloatField(column_name='outTemp', null=True)
    out_temp_battery_status = FloatField(column_name='outTempBatteryStatus', null=True)
    pressure = FloatField(null=True)
    radiation = FloatField(null=True)
    rain = FloatField(null=True)
    rain_battery_status = FloatField(column_name='rainBatteryStatus', null=True)
    rain_rate = FloatField(column_name='rainRate', null=True)
    reference_voltage = FloatField(column_name='referenceVoltage', null=True)
    rx_check_percent = FloatField(column_name='rxCheckPercent', null=True)
    soil_moist1 = FloatField(column_name='soilMoist1', null=True)
    soil_moist2 = FloatField(column_name='soilMoist2', null=True)
    soil_moist3 = FloatField(column_name='soilMoist3', null=True)
    soil_moist4 = FloatField(column_name='soilMoist4', null=True)
    soil_temp1 = FloatField(column_name='soilTemp1', null=True)
    soil_temp2 = FloatField(column_name='soilTemp2', null=True)
    soil_temp3 = FloatField(column_name='soilTemp3', null=True)
    soil_temp4 = FloatField(column_name='soilTemp4', null=True)
    supply_voltage = FloatField(column_name='supplyVoltage', null=True)
    tx_battery_status = FloatField(column_name='txBatteryStatus', null=True)
    us_units = IntegerField(column_name='usUnits')
    wind_battery_status = FloatField(column_name='windBatteryStatus', null=True)
    wind_dir = FloatField(column_name='windDir', null=True)
    wind_gust = FloatField(column_name='windGust', null=True)
    wind_gust_dir = FloatField(column_name='windGustDir', null=True)
    wind_speed = FloatField(column_name='windSpeed', null=True)
    windchill = FloatField(null=True)

    class Meta:
        table_name = 'archive'


class ArchiveDayEt(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_ET'


class ArchiveDayUv(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_UV'


class ArchiveDayMetadata(BaseModel):
    name = CharField(primary_key=True)
    value = TextField(null=True)

    class Meta:
        table_name = 'archive_day__metadata'


class ArchiveDayAltimeter(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_altimeter'


class ArchiveDayBarometer(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_barometer'


class ArchiveDayConsBatteryVoltage(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_consBatteryVoltage'


class ArchiveDayDewpoint(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_dewpoint'


class ArchiveDayExtraHumid1(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_extraHumid1'


class ArchiveDayExtraHumid2(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_extraHumid2'


class ArchiveDayExtraTemp1(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_extraTemp1'


class ArchiveDayExtraTemp2(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_extraTemp2'


class ArchiveDayExtraTemp3(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_extraTemp3'


class ArchiveDayHail(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_hail'


class ArchiveDayHailRate(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_hailRate'


class ArchiveDayHeatindex(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_heatindex'


class ArchiveDayHeatingTemp(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_heatingTemp'


class ArchiveDayHeatingVoltage(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_heatingVoltage'


class ArchiveDayInHumidity(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_inHumidity'


class ArchiveDayInTemp(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_inTemp'


class ArchiveDayInTempBatteryStatus(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_inTempBatteryStatus'


class ArchiveDayLeafTemp1(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_leafTemp1'


class ArchiveDayLeafTemp2(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_leafTemp2'


class ArchiveDayLeafWet1(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_leafWet1'


class ArchiveDayLeafWet2(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_leafWet2'


class ArchiveDayOutHumidity(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_outHumidity'


class ArchiveDayOutTemp(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_outTemp'


class ArchiveDayOutTempBatteryStatus(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_outTempBatteryStatus'


class ArchiveDayPressure(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_pressure'


class ArchiveDayRadiation(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_radiation'


class ArchiveDayRain(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_rain'


class ArchiveDayRainBatteryStatus(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_rainBatteryStatus'


class ArchiveDayRainRate(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_rainRate'


class ArchiveDayReferenceVoltage(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_referenceVoltage'


class ArchiveDayRxCheckPercent(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_rxCheckPercent'


class ArchiveDaySoilMoist1(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_soilMoist1'


class ArchiveDaySoilMoist2(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_soilMoist2'


class ArchiveDaySoilMoist3(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_soilMoist3'


class ArchiveDaySoilMoist4(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_soilMoist4'


class ArchiveDaySoilTemp1(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_soilTemp1'


class ArchiveDaySoilTemp2(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_soilTemp2'


class ArchiveDaySoilTemp3(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_soilTemp3'


class ArchiveDaySoilTemp4(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_soilTemp4'


class ArchiveDaySupplyVoltage(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_supplyVoltage'


class ArchiveDayTxBatteryStatus(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_txBatteryStatus'


class ArchiveDayWind(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    dirsumtime = IntegerField(null=True)
    max = FloatField(null=True)
    max_dir = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    squaresum = FloatField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsquaresum = FloatField(null=True)
    wsum = FloatField(null=True)
    xsum = FloatField(null=True)
    ysum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_wind'


class ArchiveDayWindBatteryStatus(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_windBatteryStatus'


class ArchiveDayWindDir(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_windDir'


class ArchiveDayWindGust(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_windGust'


class ArchiveDayWindGustDir(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_windGustDir'


class ArchiveDayWindSpeed(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_windSpeed'


class ArchiveDayWindchill(BaseModel):
    count = IntegerField(null=True)
    date_time = AutoField(column_name='dateTime')
    max = FloatField(null=True)
    maxtime = IntegerField(null=True)
    min = FloatField(null=True)
    mintime = IntegerField(null=True)
    sum = FloatField(null=True)
    sumtime = IntegerField(null=True)
    wsum = FloatField(null=True)

    class Meta:
        table_name = 'archive_day_windchill'


def init_db(name, type_="sqlite", config=None):
    config = config or {}
    drivers = {
        "sqlite": SqliteDatabase,
        "mysql": MySQLDatabase,
    }

    try:
        cls = drivers[type_]
    except KeyError:
        raise ValueError("Unknown database type: {}".format(type_)) from None
    del config["database"]
    db = cls(name, **config)
    return db
