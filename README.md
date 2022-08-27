DMS2
====

This is a little helper class for accessing a Samsung DMS2 A/C controller. It is far from feature complete, but 
should give you an idea about how to extend it.

First you need to initialize a `DMS2` object and login:

    from dms2 import DMS2

    dms2 = DMS2("https://example.com")
    dms2.login("username", "password")

Change `example.com` to whatever Hostname/IP is accessible by.

Then you can send commands:

    dms2.control(["11.00.00", "12.00.00"], {"power": "on", "setTemp": 20})

This example switches two units (`11.00.00` and `12.00.00`) on and sets their temperature to 20 degrees.

You can easily find out the names of the parameters:

    monitoring = dms2.get_monitoring()
    print(monitoring)

