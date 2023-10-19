import { XMarkIcon } from "@heroicons/react/24/solid";
import { Card, Icon } from "@tremor/react";
function Modal({
  open,
  onOpenChange,
  children,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  children: React.ReactNode;
}) {
  if (!open) {
    return null;
  }
  return (
    <Card className="absolute z-[100]  top-1/2 right-1/2 translate-x-1/2 -translate-y-1/2 p-5 bg-white max-w-xl">
      <Icon
        size="md"
        icon={XMarkIcon}
        className="absolute top-0 right-0"
        onClick={() => onOpenChange(false)}
      />
      {children}
    </Card>
  );
}

export default Modal;
