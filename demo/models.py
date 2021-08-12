from django.db import models
import datetime
from django.db import connection


class ModelBase(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def is_exists(cls):
        return cls._meta.db_table in connection.introspection.table_names()

    @classmethod
    def delete_all(cls):
        '''
        大数据量时drop比delete效率高很多
        :return:
        '''
        cls.create_model(re_create=True)

    @classmethod
    def create_model(cls, re_create=False):
        if cls.is_exists():
            if not re_create:
                return True
            with connection.schema_editor() as schema_editor:
                schema_editor.delete_model(cls)
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(cls)

    @classmethod
    def delete_model(cls, re_create=True):
        if cls.is_exists():
            with connection.schema_editor() as schema_editor:
                schema_editor.delete_model(cls)

    @classmethod
    def count(cls):
        return cls.objects.count()

    @classmethod
    def bulk_create(cls, queryset_list, batches_size=5000):
        return cls.objects.bulk_create(queryset_list, batch_size=batches_size)

    @classmethod
    def delete_all(cls):
        if cls.is_exists():
            with connection.schema_editor() as schema_editor:
                schema_editor.delete_model(cls)

    def to_dict(self, fields=None):
        if fields is None:
            fields = []
            for field in self._meta.fields:
                fields.append(field.name)
        d = {}
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                d[attr] = getattr(self, attr)
        return d


DIM = 50
FIFLD_PREV = 'P'


def testDataModel():
    modelName = 'TestData'

    class Meta:
        db_table = 'test_data'

    attrs = {
        '__module__': __name__,
        '__qualname__': modelName,
        'Meta': Meta,
        'id': models.AutoField(verbose_name='ID', primary_key=True),
        'label': models.CharField(verbose_name='时间', max_length=125, null=True),
    }
    for i in range(1, DIM + 1):
        attrs['%s%s' % (FIFLD_PREV, i)] = models.FloatField(default=None, null=True)
    return type(modelName, (ModelBase,), attrs)


TestData = testDataModel()
