settings {
    logfile    = "/logs/lsyncd.log",
    statusFile = "/logs/lsyncd.status",
}

sync {
    default.rsync,
    source = "/source/",
    target = "/target/",
    exclude = { '.DS_Store' },
    rsync = {
        binary = "/usr/bin/rsync",
        archive = true,
        compress = true,
        verbose = true,
    },
    delete = false,  -- désactive la suppression
}