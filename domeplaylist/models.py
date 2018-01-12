from django.db import models

# Create your models here.


class PlayList(models.Model):

    THEME = (
        (1, 'Тематика 1'),
        (2, 'Космос'),
        (3, 'Романтика'),
    )
    # summaryfactor = models.ForeignKey(SummaryFactor, related_name="related_mzodiac", on_delete=models.CASCADE, blank=True, null=True)

    user = models.ForeignKey('domeuser.User', default=None, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    theme = models.PositiveSmallIntegerField(blank=False, null=False, choices=THEME)

    def __str__(self):
        return "id:{} {} of {}".format(self.id, self.theme, self.title)


class PlayItem(models.Model):

    playlist = models.ForeignKey(PlayList, related_name="related_plitem", on_delete=models.CASCADE, blank=True, null=True)

    title = models.CharField(max_length=250)
    text = models.TextField()
    image = models.FileField(upload_to='media/playitem_imgs/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        return "[{}] PlayItem: {}".format(self.id, self.title)
