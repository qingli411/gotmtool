#--------------------------------
# GOMTMap
#--------------------------------
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

class GOTMMap(object):

    """GOTMMap object"""

    def __init__(self, data=None, lon=None, lat=None, name=None, units=None):
        """Initialize GOTMMap

        :data: (1D numpy array) data at each location
        :lon: (1D numpy array) longitude
        :lat: (1D numpy array) latitude
        :name: (str) name of variable
        :units: (str) units of variable

        """
        self.data = data
        self.lon = lon
        self.lat = lat
        self.name = name
        self.units = units

    def __neg__(self):
        """Return the negated GOTMMap object

        """
        out = GOTMMap(data=-self.data, lon=self.lon, lat=self.lat, name=self.name, units=self.units)
        return out

    def __add__(self, other):
        """Add 'other' to a GOTMMap object

        :other: (float, int or GOTMMap object) object to be added

        """
        if isinstance(other, float) or isinstance(other, int):
            out = GOTMMap(data=self.data+other, lon=self.lon, lat=self.lat, name=self.name, units=self.units)
        elif isinstance(other, GOTMMap):
            assert self.name == other.name, "GOTMMap object to be added has a different name."
            assert self.units == other.units, "GOTMMap object to be added has a different unit."
            data = np.zeros(self.data.size)
            loc_self = list(zip(self.lon, self.lat))
            loc_other = list(zip(other.lon, other.lat))
            for idx, val in enumerate(loc_self):
                if val in loc_other:
                    idx_other = loc_other.index(val)
                    data[idx] = self.data[idx] + other.data[idx_other]
                else:
                    data[idx] = np.nan
            out = GOTMMap(data=data, lon=self.lon, lat=self.lat, name=self.name, units=self.units)
        else:
            raise TypeError('Addition is not defined between a GOTMMap object and a {} object'.format(type(other)))
        return out

    def __sub__(self, other):
        """Subtract 'other' from a GOTMMap object

        :other: (float, int, or GOTMMap object) object to be subtracted

        """
        if isinstance(other, float) or isinstance(other, int):
            out = GOTMMap(data=self.data-other, lon=self.lon, lat=self.lat, name=self.name, units=self.units)
        elif isinstance(other, GOTMMap):
            assert self.name == other.name, "GOTMMap object to be subtracted has a different name."
            assert self.units == other.units, "GOTMMap object to be subtracted has a different unit."
            data = np.zeros(self.data.size)
            loc_self = list(zip(self.lon, self.lat))
            loc_other = list(zip(other.lon, other.lat))
            for idx, val in enumerate(loc_self):
                if val in loc_other:
                    idx_other = loc_other.index(val)
                    data[idx] = self.data[idx] - other.data[idx_other]
                else:
                    data[idx] = np.nan
            out = GOTMMap(data=data, lon=self.lon, lat=self.lat, name=self.name, units=self.units)
        else:
            raise TypeError('Subtraction is not defined between a GOTMMap object and a {} object'.format(type(other)))
        return out

    def __mul__(self, other):
        """Multiply a GOTMMap object by 'other'

        :other: (float, int, or GOTMMap object) object to be multiplied

        """
        if isinstance(other, float) or isinstance(other, int):
            out = GOTMMap(data=self.data*other, lon=self.lon, lat=self.lat, name=self.name, units=self.units)
        elif isinstance(other, GOTMMap):
            data = np.zeros(self.data.size)
            loc_self = list(zip(self.lon, self.lat))
            loc_other = list(zip(other.lon, other.lat))
            for idx, val in enumerate(loc_self):
                if val in loc_other:
                    idx_other = loc_other.index(val)
                    data[idx] = self.data[idx] * other.data[idx_other]
                else:
                    data[idx] = np.nan
            out = GOTMMap(data=data, lon=self.lon, lat=self.lat, name=self.name+' * '+other.name, units=self.units+' * '+other.units)
        else:
            raise TypeError('Multiplication is not defined between a GOTMMap object and a {} object'.format(type(other)))
        return out

    def __truediv__(self, other):
        """Divide a GOTMMap object by 'other'

        :other: (float, int, or GOTMMap object) object to be divided

        """
        if isinstance(other, float) or isinstance(other, int):
            out = GOTMMap(data=self.data/other, lon=self.lon, lat=self.lat, name=self.name, units=self.units)
        elif isinstance(other, GOTMMap):
            data = np.zeros(self.data.size)
            loc_self = list(zip(self.lon, self.lat))
            loc_other = list(zip(other.lon, other.lat))
            for idx, val in enumerate(loc_self):
                if val in loc_other:
                    idx_other = loc_other.index(val)
                    data[idx] = self.data[idx] / other.data[idx_other]
                else:
                    data[idx] = np.nan
            if other.name == self.name:
                name = 'Ratio of '+self.name
                units = 'None'
            else:
                name = self.name+' / '+other.name
                units = self.units+' / '+other.units
            out = GOTMMap(data=data, lon=self.lon, lat=self.lat, name=name, units=units)
        else:
            raise TypeError('Division is not defined between a GOTMMap object and a {} object'.format(type(other)))
        return out

    def save(self, path):
        """Save GOTMMap object

        :path: (str) path of file to save
        :returns: none

        """
        np.savez(path, data=self.data, lon=self.lon, lat=self.lat, name=self.name, units=self.units)

    def load(self, path):
        """Load data to GOTMMap object

        :path: (str) path of file to load
        :returns: (GOTMMap object)

        """
        dat = np.load(path, allow_pickle=True)
        self.__init__(data=dat['data'], lon=dat['lon'], lat=dat['lat'],
                name=str(dat['name']), units=str(dat['units']))
        return self

    def masked(self, mask, mask_data=np.nan):
        """Apply mask to GOTMMap object. The mask should also be a GOTMMap object,
           with 1 for valid and 0 for invalid.

        :mask: (GOTMMap object) mask, 1 for valid, 0 for invalid
        :mask_data: (optional) values to be filled in maked points
        :return: (GOTMMap object) masked GOTMMap

        """
        if mask.data.size != self.data.size:
            raise ValueError('The dimension of mask does not match.')
        dat = self.data
        self.data = np.where(mask.data==0, mask_data, dat)
        return self

    def plot(self, ax=None, levels=None, add_colorbar=True, cmap='rainbow', **kwargs):
        """Plot scatters on a map

        :ax: (matplotlib.axes, optional) axis to plot figure on
        :leveles: (list, optional) list of levels
        :add_colorbar: (bool) do not add colorbar if False
        :cmap: (str, optional) colormap
        :**kwargs: (keyword arguments) to be passed to mpl_toolkits.basemap.scatter()
        :return: (matplotlib figure object) figure

        """
        # plot map
        projection = ccrs.PlateCarree(central_longitude=200)
        # use curret axis if not specified
        if ax is None:
            fig, m = plt.subplots(1, 1, subplot_kw={'projection': projection})
        else:
            m = ax
            m.projection = projection
            add_colorbar = False
        m.set_extent([20.0, 380.0, -72.0, 72.0], ccrs.PlateCarree())
        m.add_feature(cfeature.LAND, zorder=1, edgecolor='black', facecolor='gray')
        m.add_feature(cfeature.OCEAN, zorder=1,facecolor='lightgray')
        gl = m.gridlines(draw_labels=True)
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        gl.top_labels= False
        gl.right_labels = False

        data = self.data
        lat = self.lat
        lon = self.lon
        # shift longitude
        lon = np.where(lon < 20., lon+360., lon)
        x, y, _ = m.projection.transform_points(ccrs.PlateCarree(), lon, lat).T
        # x, y = lon, lat
        # manually mapping levels to the colormap if levels is passed in,
        # otherwise linear mapping
        if levels is not None:
            bounds = np.array(levels)
            norm = colors.BoundaryNorm(boundaries=bounds, ncolors=256)
            im = m.scatter(x, y, marker='.', s=32, c=data, norm=norm, cmap=plt.cm.get_cmap(cmap), **kwargs)
        else:
            im = m.scatter(x, y, marker='.', s=32, c=data, cmap=plt.cm.get_cmap(cmap), **kwargs)
        # add colorbar
        if add_colorbar:
            im_ratio = 144/360
            cb = fig.colorbar(im, ax=ax, fraction=0.046*im_ratio, pad=0.04)
            cb.formatter.set_powerlimits((-2, 2))
            cb.update_ticks()
        return im

    def zonal_mean(self):
        """Calculate the zonal mean.

        :returns: (numpy array) array of latitude and zonal mean data

        """
        lat_all = self.lat
        lat, counts = np.unique(lat_all, return_counts=True)
        nlat = lat.size
        val = np.zeros(nlat)
        for i in np.arange(nlat):
            if counts[i] >=5:
                tmp_arr = self.data[lat_all==lat[i]]
                val[i] = np.nanmean(tmp_arr)
            else:
                val[i] = None
        return lat, val
