import type {
  FrontendRenderer,
  FrontendRendererArgs,
} from "@streamlit/component-v2-lib";
import { StrictMode } from "react";
import { createRoot, type Root } from "react-dom/client";

import ExperienceShell, {
  type ExperienceData,
  type ExperienceState,
} from "./ExperienceShell";
import "./styles.css";

const roots = new WeakMap<FrontendRendererArgs["parentElement"], Root>();

const renderExperience: FrontendRenderer<ExperienceState, ExperienceData> = (
  args,
) => {
  const rootElement = args.parentElement.querySelector(".react-root");
  if (!rootElement) {
    throw new Error("React root element not found");
  }

  let root = roots.get(args.parentElement);
  if (!root) {
    root = createRoot(rootElement);
    roots.set(args.parentElement, root);
  }

  root.render(
    <StrictMode>
      <ExperienceShell
        data={args.data}
        setStateValue={args.setStateValue}
        setTriggerValue={args.setTriggerValue}
      />
    </StrictMode>,
  );

  return () => {
    roots.get(args.parentElement)?.unmount();
    roots.delete(args.parentElement);
  };
};

export default renderExperience;
