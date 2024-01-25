# %%
import polars as pl
import pins
# %%
# dat = pl.read_csv("Motor_Vehicle_Collisions_-_Crashes_20240124.csv")\
#     .with_columns(
#         pl.col("CRASH DATE").str.to_date("%m/%d/%Y").alias("date"),
#         pl.col("CRASH TIME").str.to_time("%H:%M").alias("time"),
#         pl.concat_str(["CRASH DATE","CRASH TIME"], separator=" ")\
#             .str.to_datetime("%m/%d/%Y %H:%M").alias("date_time"))

# dat.write_parquet("ny_crashes.parquet", compression="zstd", compression_level=15)
# %%
dat = pl.read_parquet("ny_crashes.parquet")
# %%
# Now we want to create two visuals: the number of chrashes per hour and one that shows the number of injuries per day

# %%

# %%
