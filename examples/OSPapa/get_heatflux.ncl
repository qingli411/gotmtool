; This script reads in net longwave flux, sensible heat flux and
; latent heat flux from OCS and add them together. The sum is
; required in GOTM as heatflux.
;
; Qing Li, 20171108

begin
    dataDir = "/Users/qingli/data/OCS/Papa/Papa_20100616-20150101/"
    loc_str = "50n145w"
    qlatfile = "qlat"+loc_str+"_hr.cdf"
    qsenfile = "qsen"+loc_str+"_hr.cdf"
    lwnetfile = "lwnet"+loc_str+"_hr.cdf"
    outFile = "heatflux_hr.nc"
    f_qlat = addfile(dataDir+qlatfile, "r")
    qlat = f_qlat->QL_137
    time = f_qlat->time
    depth = f_qlat->depth
    lat = f_qlat->lat
    lon = f_qlat->lon
    f_qsen = addfile(dataDir+qsenfile, "r")
    qsen = f_qsen->QS_138
    f_lwnet = addfile(dataDir+lwnetfile, "r")
    lwnet = f_lwnet->LWN_1136
    missingvalue = f_qlat@missing_value

    HFLUX = -lwnet-qsen-qlat
    lwnet@_FillValue = missingvalue
    qsen@_FillValue = missingvalue
    qlat@_FillValue = missingvalue
    HFLUX = where(ismissing(lwnet), missingvalue, HFLUX)
    HFLUX = where(ismissing(qsen),  missingvalue, HFLUX)
    HFLUX = where(ismissing(qlat),  missingvalue, HFLUX)
    HFLUX!0 = "time"
    HFLUX&time = time
    HFLUX!1 = "depth"
    HFLUX&depth = depth
    HFLUX!2 = "lat"
    HFLUX&lat = lat
    HFLUX!3 = "lon"
    HFLUX&lon = lon
    HFLUX@long_name = "Heat flux (Sum of sensible, latent and longwave, negative for net outgoing)"
    HFLUX@units = "W m-2"

    system("rm -rf "+dataDir+outFile)
    out = addfile(dataDir+outFile, "c")
    out@history = "Generated from "+lwnetfile+", "+qsenfile+" and "+qlatfile
    out@author = "Qing Li"
    out@code = "ocs_heatflux.ncl"
    out@missing_value = missingvalue
    out@_FillValue = missingvalue
    out->HFLUX = HFLUX
    out->time = time
    out->depth = depth
    out->lat = lat
    out->lon = lon
end
