from ingestion.pipeline import ingest_message


async def index_channel(channel):
    print(f"\nIndexing #{channel.name}")

    indexed = 0
    skipped = 0

    async for message in channel.history(
        limit=None,
        oldest_first=True
    ):

        success = ingest_message(message)

        if success:
            indexed += 1

            if indexed % 100 == 0:
                print(
                    f"[{channel.name}] Indexed {indexed} messages..."
                )

        else:
            skipped += 1

    print(
        f"Finished #{channel.name} | "
        f"Indexed: {indexed} | "
        f"Skipped: {skipped}"
    )


async def index_guild(guild):

    print(f"Indexing Server: {guild.name}")

    total_channels = 0

    for channel in guild.text_channels:

        try:
            await index_channel(channel)
            total_channels += 1

        except Exception as e:
            print(f"Error indexing #{channel.name}: {e}")

    print("\nServer indexing complete.")
    print(f"Channels indexed: {total_channels}")