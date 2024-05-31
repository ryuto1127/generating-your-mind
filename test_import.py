try:
    from opencensus.ext.azure.log_exporter import AzureLogHandler
    print("opencensus is installed and can be imported.")
except ImportError as e:
    print(f"ImportError: {e}")
