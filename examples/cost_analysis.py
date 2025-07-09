import core.cost as cost 

if __name__ == "__main__":
    B300X600_1 = cost.Beam(
        width=300,
        height=600,
        length=1000
    )

    print(B300X600_1.get_total_cost())